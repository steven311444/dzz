#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用微软 Edge TTS（en-US-JennyNeural 女声）生成英语课本配套跟读音频。
用法：python gen_english_audio.py [--voice en-US-JennyNeural] [--rate -10%]
"""

import argparse
import asyncio
import pathlib
import sys

import edge_tts


TRACKS = [
    (
        "01 Starter - At School.mp3",
        "-10%",
        """Shenshen, have a great day.
You too, Mum. Have a good day. Bye-bye.
Bye.
Hi! How can I help you?
Hi! I'm looking for a storybook about robots.
It's over there.
Thank you.
You're welcome.
Mr Zhong, do you have a minute?
Yes. What can I do for you?
I like Chinese kung fu very much. Can I join the Kung Fu Club?
Of course, you can.
That's great! Thank you!
Xiaojiang, would you like to visit Ms Yuan with me tomorrow?
Yes. That would be nice. When do you want to go?
Is 9 a.m. all right?
Yes, that's good.""",
    ),
    (
        "02 Starter - Study Skills.mp3",
        "-10%",
        """Shenshen, why is your English so good?
I learn new words before every class. That's a useful skill.
It sounds helpful. I'll try this. Thank you, Shenshen.
You're welcome, Xiaopu. I know a game to help us learn words. We can play it together.
Miss Li, at home I am slow at work. I eat biscuits and play chess, but forget to do my homework. I feel so bad.
Oh, don't worry. Many students have the same problem. You can make a plan.
A plan?
Yes. For example, you spend 30 minutes doing your homework. Then you give yourself 30 minutes to have fun.
That's a good idea. Thank you, Miss Li.
Hi, Xiaojiang. I believe we can find some interesting stories in the library.
Great. Then we can choose a story to be our play script.
Sure. Let's go and search for interesting stories together.
Wow, a robot. How lovely!
Yes, it's lovely and very smart. Ask it a question, and it will give you the answer. Call it Robbie, please.
Robbie, how do you spell always?
OK. A-l-w-a-y-s, always. My friend, can you spell it again?
Ah, it's amazing.""",
    ),
    (
        "03 Starter - Numbers and Months.mp3",
        "-10%",
        """First, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth.
January, February, March, April, May, June, July, August, September, October, November, December.""",
    ),
    (
        "04 Unit 1 - Topic Words.mp3",
        "-20%",
        """Gardening. Photography. Art. Storytelling. Pottery.
Reading Club. Gardening Club. Football Club. Storytelling Club. Art Club. Photography Club.""",
    ),
    (
        "05 Unit 1 - Fun Time (Clubs).mp3",
        "-10%",
        """Welcome back to school! Here are some clubs for you this term.
Monday: Reading Club, 3:30 to 5:00, in the Reading Room.
Tuesday: Art Club, 3:30 to 5:00, in Room 306.
Wednesday: Football Club, 1:30 to 3:00, on the Sports Field. Gardening Club, 3:30 to 5:00, in the School Garden.
Thursday: Storytelling Club, 3:30 to 5:30, in Room 303.
Friday: Photography Club, only for Grades 4 and 5, 1:30 to 2:30, in Room 102.
Join us! We are waiting for you!
Sound ph. Philip sees a lovely elephant in the zoo. He takes out his phone and wants to take a photo. Oops, he drops his phone and he can't take any photos.""",
    ),
    (
        "06 Unit 1 - Talking Time.mp3",
        "-10%",
        """Shenshen, it's your photo. So sweet. I love it!
Thank you, Xiaojiang. I'm glad you like it. Taking photos helps me keep the sweet moments in life. I'm going to join the Photography Club this term.
Good idea. You can meet new friends and have fun at the same time!
Look, this is Xiaopu's painting.
Wow, the night view of the Huangpu River. It's beautiful!
I love this painting too. The colours are just amazing.
Xiaopu learns how to use colours well in the Art Club. It's fun to play with colours.
That's nice. I am going to join the Art Club. I'd like to give it a try.""",
    ),
    (
        "07 Unit 1 - Story (At the Pottery Club).mp3",
        "-10%",
        """At the Pottery Club, Miss Li says, "All the brush pots are dry now. Today, you need to paint them." James gets his brush pot. "It doesn't look very nice!" "Don't worry," Miss Li says. "It's about to change." "What do you think I should paint?" James asks Xiaopu. "How about bamboo? Bamboo is one of the four noble plants in Chinese culture."
"Good idea!" James begins to paint. "Oh, it's hard to draw the leaves!" James says. "Don't give up. Draw like this!" Xiaopu shows James. At last, James makes a nice bamboo brush pot. "With your help, it becomes easier!" James says.""",
    ),
    (
        "08 Unit 2 - Topic Words.mp3",
        "-20%",
        """Traditional. Chinese yo-yo. Kite-flying. Dragon dance. Tug of war. Hopscotch.""",
    ),
    (
        "09 Unit 2 - Fun Time (Garden Party).mp3",
        "-10%",
        """Here comes our garden party on 26 September. There will be all kinds of interesting traditional games on the sports field: Chinese yo-yo playing, kite-flying, dragon dance, tug of war, hopscotch and many others. After playing each game, you can stamp your card and get a prize. Come and have a go! Let's have fun together.
Sound ar. The game card says, "Find a star, a toy car and a bar of chocolate in the garden. It's not very hard." """,
    ),
    (
        "10 Unit 2 - Talking Time (As Fast as the Wind).mp3",
        "-10%",
        """Mr Zhong, is this Shaolin kung fu?
This is changquan, Long Fist. It's the mother of many kung fu styles.
Oh, I see. Many kung fu styles come from Long Fist?
That's right!
It's amazing! There are twelve kinds of actions.
Look, what does this look like? A tree?
Correct. Stand like a pine tree. Very strong and proud.
Look at us. Three straight trees!
Excellent! Let me show you another one. What does this look like?
I know! Sit like a bell.
Clever girl! How about this?
Wow, you move so fast!
As fast as the wind. I use all my strength for every action. That's why it's so fast!""",
    ),
    (
        "11 Unit 2 - Story (The Dragon Dance).mp3",
        "-10%",
        """The students in the dragon dance team are training hard for the coming garden party. As the head of the dragon, Minmin runs very fast. "Head of the dragon, slow down! We can't keep up with you!" Xiaopu calls out at the tail of the dragon. The background music is loud. Minmin can't hear Xiaopu. He runs even faster. The players at the tail of the dragon lose control of the sticks.
"Stop!" Mr Zhong calls out. "To play well, all the students at the dragon's head, body and tail need to be in step. Minmin, listen to the music and follow it. Everyone, follow Minmin. Let's try again." This time, all the players keep the same pace and the long dragon comes to life.""",
    ),
    (
        "12 Unit 3 - Topic Words.mp3",
        "-20%",
        """Stem. Soil. Root. Leaf. Water lily. Pine cone. Morning glory.""",
    ),
    (
        "13 Unit 3 - Chant (Parts of Plants).mp3",
        "-10%",
        """The roots hold the plant in place, and take in food and water. The stem moves water up the plant, and brings water to the leaves. The leaves take in the sunlight, and grow bigger and bigger. The flowers soon come out, and grow into a fruit holding seeds. The seeds fall into the soil, and a new plant grows.
Sound ow and ou. How can I get to the flower garden, please? Just go down the street and turn around the corner.""",
    ),
    (
        "14 Unit 3 - Talking Time (Botanical Gardens).mp3",
        "-10%",
        """Wow, the tulips are so beautiful!
The wall is covered with plants. They're creepers. They have short, thick stems. They can grow all over a wall in a very short time.
This one looks like an ice cream cone. It has a long stem and big leaves.
Look at the name tag. It's called an ice cream tulip. How lovely!
That's my favourite flower.
Look! That plant has special leaves, like a mouth with many teeth!
It's a meat-eating plant. It eats small insects.
Ah, water lilies. These broad leaves look like lovely green umbrellas. Look, the pink flowers are so beautiful!
The flowers grow from the mud under the water. But they are still clean and beautiful. Isn't it amazing?""",
    ),
    (
        "15 Unit 3 - Reading (Plants and the Weather).mp3",
        "-10%",
        """Can plants tell us about the weather? The marvel of Peru, or the four-o'clock flower, can tell you about the day's weather. If the flowers close up or fade early in the morning, it is going to be a sunny day. If the flowers are still open after 6 a.m., it is going to be cloudy or rainy.
Some plants react to weather changes. For example, on sunny days, pine cones' scales are open. On rainy days, they fold their scales to protect their seeds. Morning glory petals open during nice days, but close tightly when rain is coming. Many other plants are wonderful weather reporters too. Can you find out some of them?""",
    ),
    (
        "16 Unit 4 - Topic Words.mp3",
        "-20%",
        """Tiger. Lion. Whale. Protect. Safari park. Giraffe. Panda. Hippo. Elephant.""",
    ),
    (
        "17 Unit 4 - Fun Time (Safari Park).mp3",
        "-10%",
        """Dear children, welcome to the Safari Park. Come and get a better understanding of the animals with us. You can find out the interesting habits of animals like tigers, lions and elephants. You can learn about the threats to sea animals like whales and dolphins. Come and interact with these animals. And enjoy other fun activities here.
What to wear: closed-toe shoes, a hat, warm clothing and a raincoat. What to bring: a water bottle and an umbrella. Don't forget to take them home. How to behave: respect, care for and protect animals.
Sound ear, wear, ere, there, air, hair. Black hair, Claire is standing on the stair. What are you watching over there? A big bear in an airplane is flying in the air.""",
    ),
    (
        "18 Unit 4 - Talking Time (In a Safari Park).mp3",
        "-10%",
        """I love this safari truck tour. I feel so close to all the animals.
I do too. Look at the beautiful flamingos there. Not all of them are pink.
Now I know pandas eat more than bamboos.
Look! Mommy giraffes are taking care of their babies.
How sweet! Is that animal keeper trying to feed the giraffes?
Well, he's going to give the baby giraffes injections to keep them healthy. He tries to get closer to them with their favourite food. See? They are good friends.
Yes. We're all friends to animals.""",
    ),
    (
        "19 Unit 4 - Reading (Animal Observation Diary).mp3",
        "-10%",
        """Monday, 28 March, Sunny. Sangsang is a panda cub. I saw her birth last week. She looks different from her mother. She isn't black and white, but pink with a little bit of white hair. She can't open her eyes, but she can crawl. She is so lovely!
Saturday, 16 April, Cloudy. Momo, the hippo is one month old. He spends the day resting in water. He can walk in the water. At night, he goes with his mother to sleep on land. Momo is learning how to dive. Today, I saw Momo keeping his head under water for 5 minutes.
Tuesday, 31 May, Cloudy. Kangkang is a nineteen-year-old Asian elephant. In eight months, she will give birth to a little baby. At noon, I saw her standing under the tree and sleeping. In the afternoon, I fed her grass and leaves. She ate a lot!""",
    ),
    (
        "20 Unit 5 - Topic Words.mp3",
        "-20%",
        """Doctor. Nurse. Fever. Runny nose. Cough. Flu. Medicine.""",
    ),
    (
        "21 Unit 5 - Rhyme (Nice Doctors).mp3",
        "-10%",
        """My arm hurts badly, so I come to see Dr Cai. He is very nice and says kindly, "I know it hurts. It's OK to cry." He treats the wound carefully. "Try not to touch it. And keep it dry. Let it heal up nicely."
My nose is runny and I cough badly, so I come to see Dr Li. A nurse takes my temperature, and Dr Li is very nice and says gently, "You have a fever. And it's the flu. Take some medicine and have a good rest. Drink lots of water. And take it easy." """,
    ),
    (
        "22 Unit 5 - Talking Time (At the Eye Clinic).mp3",
        "-10%",
        """How can I help you?
Doctor, I can't see clearly these days.
Let me check your eyes. Do you watch TV or play computer games a lot?
Yes, I do.
Well, I'm afraid you use your eyes too much.
What should I do then? Can you give me some medicine for my eyes, please?
There is no need for medicine, young man. You need to watch less TV and play fewer computer games. Go out and do your favourite outdoor activities more. For example, you can go cycling or play football more. They are good for your eyes. And don't forget to do eye exercises twice a day.
Thank you, doctor. I will take good care of my eyes.""",
    ),
    (
        "23 Unit 5 - Story (The Story of Hua Tuo).mp3",
        "-10%",
        """"Ouch! Ouch!" The patient cried. "How can I reduce his pain during the treatment?" Hua Tuo thought. One day, Hua Tuo had a patient with a broken leg. The man broke his leg after drinking. During the whole treatment, the man stayed asleep. Hua Tuo was surprised. He had an idea: "I need some medicine to keep my patients asleep during the treatment."
A few days later, a mother came in with a child in her arms. The child ate some white flowers by mistake, and his mother couldn't wake him up. But an hour later, the boy woke up by himself, and everything was OK with him. The white flower was choumazi. With this plant, Hua Tuo created a medicine called mafeisan. It helped many patients in need of operation.""",
    ),
]


async def synthesize(name: str, text: str, voice: str, rate: str, out_dir: pathlib.Path) -> None:
    path = out_dir / name
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(path))
    print(f"OK: {name}")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", default="en-US-JennyNeural")
    parser.add_argument("--rate", default="-10%")
    parser.add_argument("--track", type=int, default=0, help="只生成指定序号（1 起）的音频")
    args = parser.parse_args()

    out_dir = pathlib.Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)

    tracks = TRACKS[args.track - 1 : args.track] if args.track else TRACKS
    for name, rate, text in tracks:
        try:
            await synthesize(name, text, args.voice, rate, out_dir)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: {name}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
