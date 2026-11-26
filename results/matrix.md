| case | AckMode | lab mode | deliveries | ACKs sent by lab | final status | action codes logged | sender receives | wall time |
|---|---|---|---:|---:|---|---|---|---:|
| default | Immed | AA | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| default | Immed | AE | 1 | 1 | Suspended | S | CA (IRIS) | 2s |
| default | Immed | AR | 6 | 6 | Error | RF,RF,RF,RF,RF,RF,RF | CA (IRIS) | 10s |
| default | Immed | AR3 | 6 | 6 | Error | RF,RF,RF,RF,RF,RF,RF | CA (IRIS) | 10s |
| default | Immed | OTHERID | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| default | Immed | NOMSA | 1 | 1 | Suspended | S | CA (IRIS) | 2s |
| default | Immed | NOFRAME | 1 | 1 | Error |  | CA (IRIS) | 6s |
| default | Immed | CLOSE | 6 | 0 | Error |  | CA (IRIS) | 10s |
| default | Immed | LATE | 2 | 2 | Error |  | CA (IRIS) | 11s |
| failrej | Immed | AA | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| failrej | Immed | AE | 1 | 1 | Suspended | S | CA (IRIS) | 2s |
| failrej | Immed | AR | 1 | 1 | Error | F | CA (IRIS) | 2s |
| failrej | Immed | AR3 | 1 | 1 | Error | F | CA (IRIS) | 2s |
| failrej | Immed | OTHERID | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| failrej | Immed | NOMSA | 1 | 1 | Suspended | S | CA (IRIS) | 2s |
| failrej | Immed | NOFRAME | 1 | 1 | Error |  | CA (IRIS) | 6s |
| failrej | Immed | CLOSE | 6 | 0 | Error |  | CA (IRIS) | 11s |
| failrej | Immed | LATE | 2 | 2 | Error |  | CA (IRIS) | 11s |
| legacy | Immed | AA | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| legacy | Immed | AE | 1 | 1 | Completed | CW | CA (IRIS) | 2s |
| legacy | Immed | AR | 1 | 1 | Completed | CW | CA (IRIS) | 2s |
| legacy | Immed | AR3 | 1 | 1 | Completed | CW | CA (IRIS) | 2s |
| legacy | Immed | OTHERID | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| legacy | Immed | NOMSA | 1 | 1 | Error | F | CA (IRIS) | 2s |
| legacy | Immed | NOFRAME | 1 | 1 | Error |  | CA (IRIS) | 6s |
| legacy | Immed | CLOSE | 6 | 0 | Error |  | CA (IRIS) | 10s |
| legacy | Immed | LATE | 2 | 2 | Error |  | CA (IRIS) | 10s |
| app.default | App | AA | 1 | 1 | Completed |  | AA (lab) | 2s |
| app.default | App | AE | 1 | 1 | Suspended | S | nothing | 17s |
| app.default | App | AR | 6 | 6 | Error | RF,RF,RF,RF,RF,RF,RF,RF | CE (IRIS) | 12s |
| app.default | App | AR3 | 6 | 6 | Error | RF,RF,RF,RF,RF,RF,RF,RF | CE (IRIS) | 12s |
| app.default | App | OTHERID | 1 | 1 | Completed |  | AA (lab) | 2s |
| app.default | App | NOMSA | 1 | 1 | Suspended | S | nothing | 17s |
| app.default | App | NOFRAME | 1 | 1 | Error |  | CE (IRIS) | 7s |
| app.default | App | CLOSE | 6 | 0 | Error |  | CE (IRIS) | 12s |
| app.default | App | LATE | 2 | 2 | Error |  | CE (IRIS) | 12s |
| app.failrej | App | AA | 1 | 1 | Completed |  | AA (lab) | 2s |
| app.failrej | App | AE | 1 | 1 | Suspended | S | nothing | 17s |
| app.failrej | App | AR | 1 | 1 | Error | F,F | CE (IRIS) | 2s |
| app.failrej | App | AR3 | 1 | 1 | Error | F,F | CE (IRIS) | 2s |
| app.failrej | App | OTHERID | 1 | 1 | Completed |  | AA (lab) | 2s |
| app.failrej | App | NOMSA | 1 | 1 | Suspended | S | nothing | 17s |
| app.failrej | App | NOFRAME | 1 | 1 | Error |  | CE (IRIS) | 7s |
| app.failrej | App | CLOSE | 6 | 0 | Error |  | CE (IRIS) | 12s |
| app.failrej | App | LATE | 2 | 2 | Error |  | CE (IRIS) | 12s |
| app.legacy | App | AA | 1 | 1 | Completed |  | AA (lab) | 2s |
| app.legacy | App | AE | 1 | 1 | Completed | CW | AE (lab) | 2s |
| app.legacy | App | AR | 1 | 1 | Completed | CW | AR (lab) | 2s |
| app.legacy | App | AR3 | 1 | 1 | Completed | CW | AR (lab) | 2s |
| app.legacy | App | OTHERID | 1 | 1 | Completed |  | AA (lab) | 2s |
| app.legacy | App | NOMSA | 1 | 1 | Error | F,F | CE (IRIS) | 2s |
| app.legacy | App | NOFRAME | 1 | 1 | Error |  | CE (IRIS) | 7s |
| app.legacy | App | CLOSE | 6 | 0 | Error |  | CE (IRIS) | 12s |
| app.legacy | App | LATE | 2 | 2 | Error |  | CE (IRIS) | 12s |
| msh.failrej+AL | Msh | AA | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| msh.failrej+AL | Msh | AE | 1 | 1 | Suspended | S | CA (IRIS) | 2s |
| msh.failrej+AL | Msh | AR | 1 | 1 | Error | F | CA (IRIS) | 2s |
| msh.failrej+AL | Msh | AR3 | 1 | 1 | Error | F | CA (IRIS) | 2s |
| msh.failrej+AL | Msh | OTHERID | 1 | 1 | Completed |  | CA (IRIS) | 2s |
| msh.failrej+AL | Msh | NOMSA | 1 | 1 | Suspended | S | CA (IRIS) | 2s |
| msh.failrej+AL | Msh | NOFRAME | 1 | 1 | Error |  | CA (IRIS) | 6s |
| msh.failrej+AL | Msh | CLOSE | 6 | 0 | Error |  | CA (IRIS) | 10s |
| msh.failrej+AL | Msh | LATE | 2 | 2 | Error |  | CA (IRIS) | 11s |
| msh.failrej+App | Msh | AA | 1 | 1 | Completed |  | AA (lab) | 2s |
| msh.failrej+App | Msh | AE | 1 | 1 | Suspended | S | nothing | 17s |
| msh.failrej+App | Msh | AR | 1 | 1 | Error | F,F | CE (IRIS) | 2s |
| msh.failrej+App | Msh | AR3 | 1 | 1 | Error | F,F | CE (IRIS) | 2s |
| msh.failrej+App | Msh | OTHERID | 1 | 1 | Completed |  | AA (lab) | 2s |
| msh.failrej+App | Msh | NOMSA | 1 | 1 | Suspended | S | nothing | 17s |
| msh.failrej+App | Msh | NOFRAME | 1 | 1 | Error |  | CE (IRIS) | 7s |
| msh.failrej+App | Msh | CLOSE | 6 | 0 | Error |  | CE (IRIS) | 12s |
| msh.failrej+App | Msh | LATE | 2 | 2 | Error |  | CE (IRIS) | 12s |
| msh.failrej | Msh | AA | 1 | 1 | Completed |  | nothing | 17s |
| msh.failrej | Msh | AE | 1 | 1 | Suspended | S | nothing | 17s |
| msh.failrej | Msh | AR | 1 | 1 | Error | F | nothing | 17s |
| msh.failrej | Msh | AR3 | 1 | 1 | Error | F | nothing | 17s |
| msh.failrej | Msh | OTHERID | 1 | 1 | Completed |  | nothing | 17s |
| msh.failrej | Msh | NOMSA | 1 | 1 | Suspended | S | nothing | 17s |
| msh.failrej | Msh | NOFRAME | 1 | 1 | Error |  | nothing | 17s |
| msh.failrej | Msh | CLOSE | 6 | 0 | Error |  | nothing | 17s |
| msh.failrej | Msh | LATE | 2 | 2 | Error |  | nothing | 17s |
| never.failrej | Never | AA | 1 | 1 | Completed |  | nothing | 17s |
| never.failrej | Never | AE | 1 | 1 | Suspended | S | nothing | 17s |
| never.failrej | Never | AR | 1 | 1 | Error | F | nothing | 17s |
| never.failrej | Never | AR3 | 1 | 1 | Error | F | nothing | 17s |
| never.failrej | Never | OTHERID | 1 | 1 | Completed |  | nothing | 17s |
| never.failrej | Never | NOMSA | 1 | 1 | Suspended | S | nothing | 17s |
| never.failrej | Never | NOFRAME | 1 | 1 | Error |  | nothing | 17s |
| never.failrej | Never | CLOSE | 6 | 0 | Error |  | nothing | 17s |
| never.failrej | Never | LATE | 2 | 2 | Error |  | nothing | 17s |
| byte.failrej | Byte | AA | 1 | 1 | Completed |  | byte 0x06 | 2s |
| byte.failrej | Byte | AE | 1 | 1 | Suspended | S | byte 0x06 | 2s |
| byte.failrej | Byte | AR | 1 | 1 | Error | F | byte 0x06 | 2s |
| byte.failrej | Byte | AR3 | 1 | 1 | Error | F | byte 0x06 | 2s |
| byte.failrej | Byte | OTHERID | 1 | 1 | Completed |  | byte 0x06 | 2s |
| byte.failrej | Byte | NOMSA | 1 | 1 | Suspended | S | byte 0x06 | 2s |
| byte.failrej | Byte | NOFRAME | 1 | 1 | Error |  | byte 0x06 | 6s |
| byte.failrej | Byte | CLOSE | 6 | 0 | Error |  | byte 0x06 | 11s |
| byte.failrej | Byte | LATE | 2 | 2 | Error |  | byte 0x06 | 10s |
