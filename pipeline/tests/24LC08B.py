test = {
    "hardware" : ["3", "4","5"],#hardware versions to test. DEFAULT: ALL
    "device" : "24LC04B",		#name of this test
    "position" : None,			#where on the test rig chain, None (null) for no test rig
    "test" : 
	[
		{
			"name" :"setup",
			"steps":
			[
                {
                    #"hardware" : ["3", "4", "5"],	#this command, versions applies to. DEFAULT: ALL
                    #"linefeed" : True,				#with <enter> after each command? DEFAULT: True
                    "commands" : [
                        "m",	#mode
                        "4", 	#I2C
                        "1",	#speed select
                    ]
                },
                {
                    "hardware" : ["3"],
                    "commands" : [
                        "P",	#pullups on
                        "W", 	#power on
                    ]
                },
                {
                    "hardware" : ["4", "5"],
                    "commands" : [
                        "P",	#pullups on
                        "3",	#3.3volt pullups
                        "W", 	#power on
                    ]
                }

            ]
        },
		{
			"name":"unlock",
            "steps":
			[
                {
                    "commands" : [
                        "a",	#unlock with aux pin
                    ]
                }

            ]
        },
		{
			"name":"write",
            "steps":
			[
                {
                    "commands" : [
                        "[0xa0 0 0 1 2 3 4 5 6 7 8]",	#write data to eeprom
                    ]
                }

            ]
        },
		{
			"name":"read",
            "steps":
			[
				{
					"commands" : [
						"[0xa0 0 [ 0xa1 r:9]", 	#read back from eeprom
					]
				}
			]
        }
    ]
}