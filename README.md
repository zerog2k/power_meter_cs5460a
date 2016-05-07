# power_meter_cs5460a
Arduino sketch for reading CS5460A-based digital power meter.

[example power meter sold by Banggood](http://www.banggood.com/Energy-Meter-Watt-Volt-Voltage-Electricity-Monitor-Analyzer-p-907127.html?p=WX0407753399201409DA)

![Image of Power meter banggood SKU089379](http://img.banggood.com/thumb/large/upload/2012/jiangjunchao/SKU089379/yuan/SKU089379 (1).jpg)

## Warning
Ground reference of PCB inside meter is tied to HOT (Line). It is at mains level. 
Use galvanic isolation, e.g. optocouplers, etc if you want to wire this up directly to something else.
Be sure you know what your are doing around potentially lethal mains-level voltages. Use at your own risk!

## hardware
- Arduino Pro-Mini 3.3v
- NRF24L01+ radio module
- Arduino pin 2 is connected to CLK
- Arduino pin 3 is connected to SDO
- Grounds are common to pcb and arduino inside the enclosure (see warning above!)
- Taking 5V from 78L05 regulator to arduino Vraw in.
- using 10uF cap on both arduino Vraw and NRF24L01 VCC inputs.

## analysis
Analysis of SPI communication between oem mcu and CS5460A chip.

Saleae Logic (highly recommended!) was used to analyze the communication between original mcu and CS5460A chip.

Some captures of startup and running/recurring signals are in [(logic_analyzer_captures)] folder.

### interaction
- Refer to datasheet for complete understanding of registers and formatting of values.
- In annotations below mcu->cs5460 (SDI) is `>` while cs5460->mcu (SDO) is `<`

#### startup
```
> A0        (power-up/halt)
> 00        (reg read: config)
< 00 00 01  (config reg: DCLK=MCLK/1)
> 40 01 00 61 (reg write: config. PGA Gain 50x, IHPF=1, VHPF=1)
> 44 4A 32 DF (reg write: Ign [current chan gain]. value: 1.15935)
> 48 3E 9B 5A (reg write: Vgn [voltage chan gain]. value: 0.97823)
> 00        (reg read: config)
< 01 00 61
> 04        (reg read: Ign)
< 4A 32 DF
> 08        (reg read: Vgn)    
< 3E 9B 5A
> 0A        (reg read: Cycle Count)
< 00 0F A0  (4000 = 1/sec)
> E8        (start conversion, continuous)
```
#### repeating 1 second loop
```
> 1E        (reg read: status)
< 10 03 C1  (DRDY=0)
```
... repeats query until conversion is done (DRDY=1)...
```
> 1E
< 90 03 C1  (DRDY=1)
> 5E 80 00 00  (reg write: status - clear DRDY)
> 18        (reg read: Vrms
< 2C CA 01
> 16        (reg read: Irms)
< 00 2B 7A  
> 14        (reg read: E [energy])
< FF FE 26
```

## references
[Karl Hagstrom's article](http://gizmosnack.blogspot.com/2014/10/power-plug-energy-meter-hack.html)

[CS5460A Datasheet](http://www.cirrus.com/en/pubs/proDatasheet/CS5460A_F5.pdf)

