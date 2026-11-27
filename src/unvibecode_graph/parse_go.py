"""Go syntax helpers and the usage collector (tree-sitter Go AST -> "usages").

GoUsageCollector walks one file with a scope environment, name -> type hint
(or None when the name is local but its type is unknown), and records every
use that another file might satisfy:

    {"kind": "selector",          "qualifier": "pkg", "symbol": "Name", "context": "call"|"value"}
    {"kind": "qualified_type",    "qualifier": "pkg", "symbol": "Type"}
    {"kind": "same_package_call", "name": "helper"}
    {"kind": "method_call",       "receiver": "x", "receiver_type": hint, "symbol": "Do"}

A name bound in scope is never mistaken for a package qualifier. golinks.py
resolves these against the package catalog.
"""
from __future__ import annotations

from typing import Any

from .util import child_by_field_name, line_range_from_ts_node, named_children, node_text, walk_ts

Hint = dict[str, Any] | None  # {"kind": "named"|"call", "name": ..., "qualifier": ...}
Env = dict[str, Hint]


def go_is_exported(name: str) -> bool:
    return bool(name) and name[0].isupper()


def go_is_package_level(node: Any) -> bool:
    parent = getattr(node, "parent", None)
    while parent is not None:
        if parent.type in {"function_declaration", "method_declaration", "func_literal"}:
            return False
        parent = getattr(parent, "parent", None)
    return True


def go_receiver_type(node: Any, source_bytes: bytes) -> str | None:
    """Method declaration -> its receiver's type name ('*Repo' and 'Repo' both give 'Repo')."""
    for child in named_children(node):
        if child.type == "parameter_list":
            for desc in walk_ts(child):
                if desc.type == "type_identifier":
                    return node_text(desc, source_bytes).strip()
            break
    return None


def go_named_type(node: Any, source_bytes: bytes) -> str | None:
    """Type node -> 'Name' or 'pkg.Name', looking through pointers, generics and parentheses."""
    if node is None:
        return None
    if node.type == "type_identifier":
        return node_text(node, source_bytes).strip()
    if node.type == "qualified_type":
        package_node = child_by_field_name(node, "package")
        name_node = child_by_field_name(node, "name")
        if package_node is None or name_node is None:
            children = named_children(node)
            if len(children) >= 2:
                package_node, name_node = children[0], children[1]
        if package_node is not None and name_node is not None:
            package_name = node_text(package_node, source_bytes).strip()
            type_name = node_text(name_node, source_bytes).strip()
            if package_name and type_name:
                return f"{package_name}.{type_name}"
        return None
    if node.type in {"pointer_type", "generic_type", "parenthesized_type", "variadic_parameter_declaration"}:
        inner = child_by_field_name(node, "type")
        if inner is None:
            children = named_children(node)
            inner = children[0] if children else None
        return go_named_type(inner, source_bytes)
    if node.type == "parameter_list":
        parameters = [
            child
            for child in named_children(node)
            if child.type in {"parameter_declaration", "variadic_parameter_declaration"}
        ]
        if parameters:
            return go_named_type(child_by_field_name(parameters[0], "type"), source_bytes)
    return None


SCOPES = {
    "block", "for_statement", "if_statement", "expression_switch_statement", "select_statement",
    "expression_case", "type_case", "default_case", "communication_case",
}
USAGE_KEY = ("kind", "qualifier", "receiver", "name", "symbol", "context", "line")
PREDECLARED_TYPES = {
    "any", "bool", "byte", "comparable", "complex64", "complex128", "error", "float32", "float64",
    "int", "int8", "int16", "int32", "int64", "rune", "string",
    "uint", "uint8", "uint16", "uint32", "uint64", "uintptr",
}


class GoUsageCollector:
    def __init__(self, source_bytes: bytes) -> None:
        self.source_bytes = source_bytes
        self.usages: list[dict[str, Any]] = []
        self.visitors = {
            "function_declaration": self._function,
            "method_declaration": self._function,
            "func_literal": self._function,
            **{node_type: self._scope for node_type in SCOPES},
            "short_var_declaration": self._short_var,
            "var_spec": self._var_spec,
            "const_spec": self._var_spec,
            "range_clause": self._range,
            "type_switch_statement": self._type_switch,
            "call_expression": self._call,
            "type_conversion_expression": self._conversion,
            "selector_expression": self._selector,
            "qualified_type": self._qualified_type,
            "type_identifier": self._type_identifier,
        }

    def collect(self, root: Any) -> list[dict[str, Any]]:
        self.visit(root, {})
        seen, unique = set(), []
        for usage in self.usages:
            key = tuple(usage.get(field) for field in USAGE_KEY)
            if key not in seen:
                seen.add(key)
                unique.append(usage)
        return unique

    def visit(self, node: Any, env: Env) -> None:
        handler = self.visitors.get(node.type)
        if handler is not None:
            handler(node, env)
            return
        for child in named_children(node):
            self.visit(child, env)

    # --- one visitor per node type ----------------------------------------

    def _function(self, node: Any, env: Env) -> None:
        """Parameters and receiver are visible in the body only."""
        local_env = dict(env)
        if node.type == "method_declaration":
            local_env.update(self._parameter_types(child_by_field_name(node, "receiver")))
        local_env.update(self._parameter_types(child_by_field_name(node, "parameters")))
        body = child_by_field_name(node, "body")
        for child in named_children(node):
            if child.type == "block":
                continue
            self.visit(child, env)
        if body is not None:
            self.visit(body, local_env)

    def _scope(self, node: Any, env: Env) -> None:
        scoped_env = dict(env)
        for child in named_children(node):
            self.visit(child, scoped_env)

    def _short_var(self, node: Any, env: Env) -> None:
        """a, b := f(), g(): visit the right side first, then bind names in this scope."""
        right = child_by_field_name(node, "right")
        if right is not None:
            self.visit(right, env)
        left = child_by_field_name(node, "left")
        names = [self._text(child) for child in (named_children(left) if left is not None else []) if child.type == "identifier"]
        values = named_children(right) if right is not None else []
        hints: list[Hint] = [None] * len(names)
        if len(values) == 1:
            hints = [self._expression_type(values[0], env)] + [None] * (len(names) - 1)
        elif len(values) == len(names):
            hints = [self._expression_type(value, env) for value in values]
        for name, hint in zip(names, hints):
            if name and name != "_":
                env[name] = hint

    def _var_spec(self, node: Any, env: Env) -> None:
        """var/const inside a function binds names; at package level it does not."""
        for child in named_children(node):
            self.visit(child, env)
        if go_is_package_level(node):
            return
        names = [self._text(child) for child in node.children if child.type == "identifier" and self._text(child) not in {"", "_"}]
        type_value = self._type_hint(child_by_field_name(node, "type"))
        value = child_by_field_name(node, "value")
        values = named_children(value) if value is not None else []
        hints: list[Hint] = [None] * len(names)
        if type_value is not None:
            hints = [type_value] * len(names)
        elif len(values) == 1:
            hints = [self._expression_type(values[0], env)] + [None] * (len(names) - 1)
        elif len(values) == len(names):
            hints = [self._expression_type(item, env) for item in values]
        for name, hint in zip(names, hints):
            env[name] = hint

    def _range(self, node: Any, env: Env) -> None:
        right = child_by_field_name(node, "right")
        if right is not None:
            self.visit(right, env)
        left = child_by_field_name(node, "left")
        if left is None:
            return
        for child in named_children(left):
            if child.type == "identifier":
                name = self._text(child)
                if name and name != "_":
                    env[name] = None

    def _type_switch(self, node: Any, env: Env) -> None:
        """switch v := x.(type): v is local, with an unknown type."""
        scoped_env = dict(env)
        for child in node.children:
            if child.type == ":=":
                break
            if child.type == "expression_list":
                for item in named_children(child):
                    if item.type == "identifier":
                        name = self._text(item)
                        if name and name != "_":
                            scoped_env[name] = None
        for child in named_children(node):
            self.visit(child, scoped_env)

    def _call(self, node: Any, env: Env) -> None:
        """f(), (f)(), x.M() and pkg.F(): record the call, then visit the arguments."""
        target = child_by_field_name(node, "function")
        while target is not None and target.type == "parenthesized_expression":
            children = named_children(target)
            target = children[0] if children else None
        arguments = child_by_field_name(node, "arguments")
        if target is not None and target.type == "identifier":
            self._same_package_call(self._text(target), node, env)
        elif target is not None and target.type == "selector_expression" and self._is_simple_selector(target):
            receiver = self._text(child_by_field_name(target, "operand"))
            if receiver in env:
                self.usages.append(
                    {
                        "kind": "method_call",
                        "receiver": receiver,
                        "receiver_type": env.get(receiver),
                        "symbol": self._text(child_by_field_name(target, "field")),
                        "line": line_range_from_ts_node(node)["start_line"],
                    }
                )
            else:
                self._package_selector(target, env, "call")
        elif target is not None:
            self.visit(target, env)
        if arguments is not None:
            self.visit(arguments, env)

    def _conversion(self, node: Any, env: Env) -> None:
        """Map[int](xs) parses as a conversion: a call to a generic function."""
        children = named_children(node)
        base = children[0] if children else None
        if base is not None and base.type == "generic_type":
            generic_children = named_children(base)
            target = generic_children[0] if generic_children else None
            if target is not None and target.type == "type_identifier":
                self._same_package_call(self._text(target), node, env)
        for child in named_children(node):
            self.visit(child, env)

    def _selector(self, node: Any, env: Env) -> None:
        self._package_selector(node, env, "value")
        for child in named_children(node):
            self.visit(child, env)

    def _qualified_type(self, node: Any, env: Env) -> None:
        package_node = child_by_field_name(node, "package")
        name_node = child_by_field_name(node, "name")
        if package_node is not None and name_node is not None:
            qualifier = self._text(package_node)
            symbol = self._text(name_node)
            if qualifier and symbol and qualifier not in env:
                self.usages.append(
                    {
                        "kind": "qualified_type",
                        "qualifier": qualifier,
                        "symbol": symbol,
                        "line": line_range_from_ts_node(node)["start_line"],
                    }
                )
        for child in named_children(node):
            self.visit(child, env)

    def _type_identifier(self, node: Any, env: Env) -> None:
        name = self._text(node)
        parent = getattr(node, "parent", None)
        if not name or name in PREDECLARED_TYPES or (parent is not None and parent.type == "qualified_type"):
            return
        self.usages.append({"kind": "same_package_type", "name": name, "line": line_range_from_ts_node(node)["start_line"]})

    # --- recording --------------------------------------------------------

    def _same_package_call(self, name: str, node: Any, env: Env) -> None:
        if name and name not in env and name not in {"init", "main"}:
            self.usages.append({"kind": "same_package_call", "name": name, "line": line_range_from_ts_node(node)["start_line"]})

    def _package_selector(self, node: Any, env: Env, context: str) -> None:
        """pkg.Name where pkg is not a local name."""
        if not self._is_simple_selector(node):
            return
        qualifier = self._text(child_by_field_name(node, "operand"))
        if not qualifier or qualifier in env:
            return
        symbol = self._text(child_by_field_name(node, "field"))
        if not symbol:
            return
        self.usages.append(
            {
                "kind": "selector",
                "qualifier": qualifier,
                "symbol": symbol,
                "context": context,
                "line": line_range_from_ts_node(node)["start_line"],
            }
        )

    # --- types --------------------------------------------------------------

    def _text(self, node: Any) -> str:
        return node_text(node, self.source_bytes).strip()

    @staticmethod
    def _is_simple_selector(node: Any) -> bool:
        """identifier.field (not a chained or indexed expression)."""
        operand = child_by_field_name(node, "operand")
        field = child_by_field_name(node, "field")
        return operand is not None and field is not None and operand.type == "identifier"

    def _type_hint(self, node: Any) -> Hint:
        name = go_named_type(node, self.source_bytes)
        if not name:
            return None
        if "." in name:
            qualifier, owner = name.split(".", 1)
            if qualifier and owner:
                return {"kind": "named", "name": owner, "qualifier": qualifier}
            return None
        return {"kind": "named", "name": name, "qualifier": None}

    def _parameter_types(self, parameter_list: Any) -> Env:
        bindings: Env = {}
        if parameter_list is None:
            return bindings
        for parameter in named_children(parameter_list):
            if parameter.type not in {"parameter_declaration", "variadic_parameter_declaration"}:
                continue
            hint = self._type_hint(child_by_field_name(parameter, "type"))
            for child in parameter.children:
                if child.type == "identifier":
                    name = self._text(child)
                    if name and name != "_":
                        bindings[name] = hint
        return bindings

    def _expression_type(self, node: Any, env: Env) -> Hint:
        """What type an expression has, as far as this file alone can tell."""
        if node is None:
            return None
        t = node.type
        if t == "expression_list":
            children = named_children(node)
            return self._expression_type(children[0], env) if len(children) == 1 else None
        if t == "identifier":
            return env.get(self._text(node))
        if t == "parenthesized_expression":
            children = named_children(node)
            return self._expression_type(children[0], env) if children else None
        if t == "unary_expression":  # &x and *x have x's type
            operator = next((child for child in node.children if child.type in {"&", "*"}), None)
            operand = child_by_field_name(node, "operand")
            if operand is None:
                children = named_children(node)
                operand = children[0] if children else None
            return self._expression_type(operand, env) if operator is not None else None
        if t == "composite_literal":
            type_node = child_by_field_name(node, "type")
            if type_node is None:
                children = named_children(node)
                type_node = children[0] if children else None
            return self._type_hint(type_node)
        if t == "type_assertion_expression":
            return self._type_hint(child_by_field_name(node, "type"))
        if t == "type_conversion_expression":
            children = named_children(node)
            base = children[0] if children else None
            if base is not None and base.type == "generic_type":
                generic_children = named_children(base)
                base = generic_children[0] if generic_children else None
            return self._type_hint(base)
        if t == "call_expression":
            return self._call_type(node, env)
        return None

    def _call_type(self, node: Any, env: Env) -> Hint:
        """new(T) -> T; F() and pkg.F() -> a 'call' hint golinks resolves via F's return type."""
        function_node = child_by_field_name(node, "function")
        if function_node is None:
            return None
        if function_node.type == "identifier":
            name = self._text(function_node)
            if name != "new":
                return {"kind": "call", "name": name, "qualifier": None}
            arguments = child_by_field_name(node, "arguments")
            if arguments is not None:
                children = named_children(arguments)
                if len(children) == 1:
                    return self._type_hint(children[0])
            return None
        if function_node.type == "selector_expression" and self._is_simple_selector(function_node):
            qualifier = self._text(child_by_field_name(function_node, "operand"))
            if qualifier in env:
                return None
            return {"kind": "call", "name": self._text(child_by_field_name(function_node, "field")), "qualifier": qualifier}
        return None
