// EEPROM test procedure to test EEPROM functionality on Teensy4.1 HW

#if !defined(UNIT_TEST)
#    error "This file must only be compiled in when in test mode"
#endif

#include <Arduino.h>

#include <unity.h>

#include <cmn/daq_common.h>
#include <eeprom/eeprom.h>

void test_eeprom_gearPos()
{
    daq_GearPos_t test_gearPos = 0U; // Neutral

    eeprom_writeGearPosition(test_gearPos);
    TEST_ASSERT_EQUAL(test_gearPos, eeprom_readGearPosition());

    test_gearPos = 6U; // Max gear number

    eeprom_writeGearPosition(test_gearPos);
    TEST_ASSERT_EQUAL(test_gearPos, eeprom_readGearPosition());

    test_gearPos = 4294967295U; // Max possible number

    eeprom_writeGearPosition(test_gearPos);
    TEST_ASSERT_EQUAL(test_gearPos, eeprom_readGearPosition());
}

void setup()
{
    delay(2000);

    UNITY_BEGIN();

    RUN_TEST(test_eeprom_gearPos);

    UNITY_END();
}

void loop()
{
    // Don't need anything in here
}