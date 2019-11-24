Hacker the Husky

By Alex, Alfi, Matthew, Ross, Tom

MOTIVATION

Part of Durham County Council’s adult social care services includes improving the daily living of elderly residents who have either mobility issues or mental health problems. However, the cost of these social care projects and personal care assistants is ever-increasing, due to an ageing population. In the year 2018/19, more than 840 000 people received publicly funded long-term adult social care. Clearly, the demand is huge, and so assistive technology is implemented to combat these issues while keeping costs to a minimum. This relieves pressure on adult social care budgets. An estimated 1.1-1.7 million people in the UK are currently supported by assistive technology, solving a variety of problems.

WHAT WE WANT TO ACHIEVE

Our idea is to create a communication-focused companion to combat loneliness in the elderly, especially those showing early signs of dementia. Many individuals in this category live alone, and therefore have little opportunity to have a conversation. It is possible that this lack of conversation could lead to a deterioration of their memory. Our device should promote a daily conversation that forces the user to interact with the toy, by recounting their activities throughout the day, for example. The Alzheimer’s Society claims that keeping the brain active by doing these sorts of exercises can improve memory and retain information for longer.

The device should follow some fundamental aims:

    • It should be easy to use
    • It should be follow some basic word triggers to execute commands and respond with one of a list of phrases.
    • It should detect a cry for help, to trigger a correspondence between the user and a family member / emergency services
    • Give reassurance to family members that their loved one can find comfort with this assistive technology

HOW WE ARE ACHIEVING THIS

Alex and Matt resource a cuddly puppy toy. Matt and Ross proceed to tear apart said toy and insert various components into its stuffing. Meanwhile, Tom is creating a speech-to-text (STT) as well as a TTS protocol for conversation between user and puppy. Alfi looks at how we can store the data in the cloud and Ross investigates how to relay information to the front end, which Alex is looking into.

Eventually, the device should address the aims by doing the following:

    • Responding to questions asked in plain English
    • Process the information and save the data in the form {speech detected, timestamp}
    • Run a function that decides how to respond
    • Occasionally move in a “cute and endearing fashion”

PROBLEMS WE RAN IN TO

Initially, we thought we could use the Google Home Mini for the microphone/speakers. However, we realised this would involve using Google’s own speech recognition software, and thus requiring the user to say Google’s start-up command ("OK Google"). This would then go against one of our key aims which is to make the technology as easy to use as possible, given the target audience.

Another problem we found was that the version of Python that the Raspberry Pi was running didn’t support some of the code, so some updates needed to be made.

Trying to fit the servos into the stuffed toy proved problematic, so a supportive frame had to be fitted inside so that the arms could be made to move. We built the frame out of chopsticks and zip ties.

We also abandoned the idea of implementing mongoDB into our database structure in favour of Google’s Cloud platform.

The microphones/speakers we had available to us either wouldn’t connect via Bluetooth or used a 3.5mm jack input which also wasn’t supported on the Raspberry Pi.
