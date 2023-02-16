            if self.mode == "midtemp":
                keyslist = list(mid_temp_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(mid_temp_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(mid_temp_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
            elif self.mode == 'midsoilwet':
                keyslist = list(mid_soil_wet_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(mid_soil_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(mid_soil_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '%   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
            if self.mode == "midairwet":
                keyslist = list(mid_air_wet_history.keys())
                self.text = '#################################\n'
                if len(keyslist) < 6:
                    for k in keyslist:
                        localvalue = str(mid_air_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
                else:
                    for k in keyslist[-6:]:
                        localvalue = str(mid_air_wet_history[k])
                        if len(localvalue) < 5:
                            localvalue += '0' * (5 - len(localvalue))
                        localtext = self.text
                        localtext += '#   ' + localvalue + '°C   #   ' + time.ctime(k + start_time) + '   #\n'
                        localtext += '#################################\n'
                        self.text = localtext
