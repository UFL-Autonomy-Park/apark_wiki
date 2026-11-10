!!! note "What a Good Fix Is for a Quadcopter"
    **A good fix is `fix_type` 6, always.** Read the `fix_type` entry of `<namespace>/mavros/gpsstatus/gps1/raw`. When everything works, every single message coming out of MAVROS shows 6 (RTK fixed) while flying around, never less.

    **This reliability is only tested up to three quadcopters** under the current setup: RTKLib on the discovery server computer. Three agents have also been tested with the Emlid RS3's embedded caster, which sends corrections over an individual link to every quadcopter (every local NTRIP client). That is **not reliable at all**: the fix drops out randomly and intermittently. Even with one agent, flying can reduce the fix to 5 from what it was on the ground, with no recovery and no explanation. **Use the RTKLib caster, never the embedded caster.**

!!! warning "Wait for the Fix to Reach 6"
    Getting a fix takes 5 to 15 minutes. Until `fix_type` reaches 6, expect lots of "Global position estimate invalid" errors. A fix of 5 (RTK float) can make flights unstable, so it is very important to wait for 6 (fixed) before you fly.

    The fix should drop to 5 or lower, even for a single frame, only if you hit the ground hard, crash, or the satellites cut out. (The satellites cut out once in 100 flight hours.) Moving fast or changing altitude should never demote the fix.

    Multi-agent testing has not been done, so it is unknown whether network traffic, or changing access points, affects the fix.

!!! tip "An Easier Way to Check the Fix"
    Click the GPS icon in the **Fly** tab of AMC (Astros) or QGC (Homebrews) to check the RTK fix.
