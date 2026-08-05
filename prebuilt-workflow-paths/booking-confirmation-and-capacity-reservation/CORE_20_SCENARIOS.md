# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Active hold confirms one booking | The hold creates duplicate bookings or capacity deductions |
| 2 | Direct booking commits available capacity | Capacity is oversold or reserved without a booking |
| 3 | Provider calendar binds same booking | Another booking or slot receives the reference |
| 4 | Required booking data is missing | An incomplete booking enters operations |
| 5 | Slot or party data is malformed | Invalid values reach capacity, payment, calendar, or logs |
| 6 | Hold or capacity is no longer valid | Stale capacity is silently committed |
| 7 | Actor cannot create booking | A hold or resource identifier grants cross-account control |
| 8 | Timezone crosses calendar boundary | The provider and customer reserve different times |
| 9 | Two customers request last capacity | Both receive exclusive confirmed capacity |
| 10 | Hold converts at expiry boundary | Both expiry and conversion change capacity |
| 11 | Confirmation response is lost | A second booking is created |
| 12 | Idempotency key is replayed with changed slot | The old key mutates or creates a different booking |
| 13 | Booking attempts are flooded | Capacity hoarding or provider cost grows unchecked |
| 14 | Booking commits but capacity update fails | The customer is confirmed without capacity |
| 15 | External provider times out | Timeout becomes false rejection or duplicate provider booking |
| 16 | Booking commits but response is lost | Confirmation and downstream effects repeat |
| 17 | Cross-tenant resource is referenced | Identifiers cross booking boundaries |
| 18 | Booking failure is logged | Protected booking details enter unsafe logs |
| 19 | Late provider rejection follows confirmation | The system stays falsely confirmed or silently loses the booking |
| 20 | Confirmation or reminder fails | The booking duplicates or the customer is misled |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

