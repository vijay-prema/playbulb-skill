# Playbulb Skill
[Mycroft](https://mycroft.ai/) skill to control a Mipow Playbulb Candle over BLE. Up to 5 bulbs can be controlled with this skill.



## Examples

* "Turn candles off"
* "Turn candles on"



## Dependencies

* [bluepy](https://github.com/IanHarvey/bluepy) (this should now be automatically installed by the skill when its added).



## Installation

```bash
mycroft-msm install https://github.com/vijay-prema/playbulb-skill
```

Find the BLE MAC addresses for all your bulbs,  and enter each address into the [skills settings](https://account.mycroft.ai/skills).  See below for help.



## Find BLE devices address

Find all local BLE devices MAC address using scan:
`sudo hcitool lescan`

You may be able to identify them just from this list either from their names, or by turning them off and on and seeing if they appear or disapear from this list.

Optionally, test the device using gatttool to check that the playbulb can be controlled over BLE:
`sudo gatttool -i hci0 -b 1A:2B:3C:4D:5E:6F -m 48 --interactive`

```
connect
characteristics
```

look for uuid `fffc` and get its handle (in my case it was  29). 

Then try turning the bulb on and off

```
char-write-cmd 29 ffffffff
char-write-cmd 29 00000000
```



## Notes and limitations

* Max number of candles is 5. This can be changed fairly easily in the code.
* The BLE range on different devices varies. I get at least 5m line of site from my Picroft running on a Rasberry Pi 3B.  On another Linux laptop I only get 2-3m.
* Sometimes BLE fails to communicate for some reason, therefore it will retry after a 1s delay on failure, and the max number of retries can be changed in settings. This can make the script a bit slow at times, especially if there are a lot of failures.
* Only turns bulbs on and off. In future I may add ability to set specific colors, effects, or create some presets.
