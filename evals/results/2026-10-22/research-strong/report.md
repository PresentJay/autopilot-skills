# Vendor comparison as of 2026-10-21

| Topic | Vendor A | Vendor B |
| --- | --- | --- |
| Latency | Reported median: **200 ms**, in a benchmark with one request at a time on a local network. [A, line 1](vendor-a.txt#L1) | **Unknown:** the specification is unavailable; the supplied file records HTTP 403. [B, line 1](vendor-b-error.txt#L1) |
| Offline support | **Unknown:** not described in the supplied specification. [A, line 1](vendor-a.txt#L1) | **Unknown:** the specification is unavailable. [B, line 1](vendor-b-error.txt#L1) |

Vendor A's supplied specification states a publication date of 2026-10-01. Its latency figure is a vendor-reported benchmark result, not an independently measured result or a guarantee under other conditions. The supplied sources do not establish whether either vendor supports offline operation; omission does not establish lack of support.

Source B's access failure prevents verification of its latency and offline support. Neither a latency ranking nor an offline-support comparison can be established. No contents of the missing specification were inferred, and no network access was attempted.

Verification: checked this report against both supplied local files and the scope in [mission.md](mission.md). Only Vendor A's stated figure, conditions, publication date, and omission, plus Source B's unavailability, could be verified from these inputs. Whether the specifications changed by 2026-10-21 is unknown.
