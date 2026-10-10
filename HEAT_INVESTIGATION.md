# Heat investigation

Open **Heat history** in the system health panel, or run `subcult-heat open`.
Sampling starts disabled. Enable it, then take a two-second sample whenever you
want to compare temperature with CPU activity. There is no background sampler.

The timeline retains at most 240 samples: temperature, up to four fan readings,
power profile, and the six busiest process groups. Samples live in
`$XDG_STATE_HOME/subcult-rice/heat-history.json` with mode 600. CPU percentages
use one core as 100%, so a process group can exceed 100%. PID start times prevent
reused PIDs from being counted as the same process.

```sh
subcult-heat enable
subcult-heat sample --seconds 2
subcult-heat history
subcult-heat disable
subcult-heat clear
```

Missing sensors or power-profile support display as unavailable. Process names
come from `/proc/*/comm`; command lines, window titles, URLs, and browser history
are never read. CPU load and temperature are correlated observations, not proof
that a particular process caused heating. No process is killed or throttled.
Existing sustained-temperature warnings keep their own thresholds and timers.
