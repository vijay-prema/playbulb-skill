# Copyright 2021 Vijay Prema.
#
# Distributed under the Apache License 2.0

import time
from mycroft import MycroftSkill, intent_handler
from bluepy.btle import UUID, Peripheral


class PlayBulbSkill(MycroftSkill):

    max_retries = 4
    candles = ['', '', '', '', '']

    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()

    def on_settings_changed(self):
        self.candles[0] = self.settings.get('candle_addr1', '')
        self.candles[1] = self.settings.get('candle_addr2', '')
        self.candles[2] = self.settings.get('candle_addr3', '')
        self.candles[3] = self.settings.get('candle_addr4', '')
        self.candles[4] = self.settings.get('candle_addr5', '')
        self.max_retries = self.settings.get('max_retries', 4)

    def send_message_to_bulb(self, message, address):
        led_service_uuid = UUID(0xfe0c)
        led_char_uuid = UUID(0xfffc)

        try:
            p = Peripheral(address)
        except:
            return False

        try:
            LedService = p.getServiceByUUID(led_service_uuid)
            ch = LedService.getCharacteristics(led_char_uuid)[0]
            ch.write(message)
        except:
            return False
        finally:
            p.disconnect()

        return True

    @intent_handler('PlaybulbOn.intent')
    def handle_play_bulb_on_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.speak("on")

        for candle in self.candles:
            if(candle != ''):
                try_again = 0
                while(try_again < self.max_retries):
                    if(self.send_message_to_bulb(b'\xff\x00\x00\x00', candle)):
                        try_again = self.max_retries
                    try_again = try_again + 1
                    time.sleep(1)

    @intent_handler('PlaybulbOff.intent')
    def handle_play_bulb_off_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.speak("off")

        for candle in self.candles:
            if(candle != ''):
                try_again = 0
                while(try_again < self.max_retries):
                    if(self.send_message_to_bulb(b'\x00\x00\x00\x00', candle)):
                        try_again = self.max_retries
                    try_again = try_again + 1
                    time.sleep(1)

    def stop(self):
        pass


def create_skill():
    return PlayBulbSkill()
