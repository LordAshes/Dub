# Ming-3.0-tts-0.5b Control Reference

English | [简体中文](instructions.md)

Every value accepted by the `controls`, `language_id` and inline-tag inputs of
`MingTTS.synthesize`. Sections marked **new** did not exist in the previous
release.

- [Paralinguistic tags](#paralinguistic-tags-new)
- [Target languages](#target-languages-new)
- [Freeform control](#freeform)
- [Speech control](#speech-control)
- [Built-in premium voices](#built-in-premium-voices)
- [Voice design](#voice-design)

## <a id="paralinguistic-tags-new"></a>Paralinguistic tags **new**

Written inline in the text, in either Chinese or English, anywhere in the
sentence. They are routed around text normalization, so they reach the model
unchanged. Tags are case-sensitive and must include the brackets.

| Tag | Effect |
| :--- | :--- |
| `[Breathing]` | audible breath |
| `[Cough]` | cough |
| `[Sigh]` | sigh |
| `[Laughter]` | laughter |
| `[Uhm]` | hesitation filler |
| `[Surprise-ah]` | surprised "ah" |
| `[Surprise-oh]` | surprised "oh" |
| `[Dissatisfaction-hnn]` | disgruntled "hnn" |
| `[Confirmation-en]` | affirming "en" |
| `[Question-ei]` | questioning "ei" |
| `[Question-ah]` | questioning "ah" |
| `[Question-en]` | questioning "en" |
| `[Question-oh]` | questioning "oh" |
| `[Question-huh]` | questioning "huh" |

## <a id="target-languages-new"></a>Target languages **new**

Passed as `language_id`. Chinese and English work without it; the other five
require it, because it both adds the target-language line to the prompt and
keeps the text away from the Chinese/English normalizer.

| `language_id` | Language |
| :--- | :--- |
| `zh` | Chinese |
| `en` | English |
| `ja` | Japanese |
| `ko` | Korean |
| `de` | German |
| `fr` | French |
| `es` | Spanish |

The voice is carried by the reference recording, not the language, so a
Chinese reference can speak any of these.

Dialects are not selected here; see the `dialect` control below.

## <a id="freeform"></a>Freeform control

Pass a natural-language delivery instruction through `instruction` to guide tone, pacing, emphasis or speaking style. Put only the words to synthesize in `text`; do not prepend the instruction to the spoken text. Reference audio is not required and is not recommended by default. Do not combine Freeform with voice design, built-in voices, emotion, dialect or basic attribute controls.

The instructions below are preserved exactly as used, including the Chinese inputs. Scenario labels are explanatory and are not model parameters.

| Scenario | Instruction (`instruction`) |
| :--- | :--- |
| English: encouraging sports coach | Sound like an encouraging sports coach, energetic and firm without shouting. |
| Chinese: gentle bedtime story | 用温柔、舒缓的声音讲述睡前故事，像在轻声安慰孩子。 |
| English: warm storytelling | Speak in a warm, intimate storytelling voice, unhurried. |

The examples assume the model has been loaded as described in the README. The synthesis texts are illustrative.

### English sports coach (0.5B)

```python
model.synthesize(
    task="FREEFORM",
    text="Keep your eyes forward and your shoulders relaxed. One more round—you can do this!",
    instruction="Sound like an encouraging sports coach, energetic and firm without shouting.",
    use_zero_spk_emb=True,
)
```

### English warm storytelling (0.5B)

```python
model.synthesize(
    task="FREEFORM",
    text="The old radio crackled softly as the storm moved across the valley.",
    instruction="Speak in a warm, intimate storytelling voice, unhurried.",
    use_zero_spk_emb=True,
)
```

### Chinese bedtime story (Tiny)

Omit `prompt_wav` and `prompt_text`.

```python
tts.generate(
    task="freeform",
    text="小熊轻轻闭上眼睛，月亮替它盖好了一床银色的被子。",
    instruction="用温柔、舒缓的声音讲述睡前故事，像在轻声安慰孩子。",
)
```

## <a id="speech-control"></a>Speech Control

Use the exact values in backticks. English glosses explain the values; they are not API aliases. Chinese voice identifiers and their emotion suffixes also remain untranslated.

| Control | Values |
| :--- | :--- |
| `emotion` | `高兴` (happy), `悲伤` (sad), `愤怒` (angry), `恐惧` (fearful), `厌恶` (disgusted), `惊讶` (surprised), `中性` (neutral) |
| `dialect` | `cantonese` (Cantonese), `chuanyu dialect` (Sichuan–Chongqing dialect) |
| `speed` | `慢速` (slow), `中速` (medium), `快速` (fast) |
| `pitch` | `低` (low), `中` (medium), `高` (high) |
| `volume` | `低` (low), `中` (medium), `高` (high) |

## <a id="built-in-premium-voices"></a>Built-in premium voices

Recommended voices are listed below. Use the exact `ip` values shown.

### Chinese voices without emotion variants

| ip | Gender | Age | Suggested roles | Voice description | Suggested uses |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `灵小安` | Female | Teenage girl | AI assistant; game guide; anime maid | Sweet, crisp and energetic, with an approachable, cute anime-style delivery. | Customer-service voice |
| `灵语汐` | Female | Teenage girl | Playful younger sister; cheerful girl | Clear, bright and youthful, with a sunny, energetic delivery. | Entertainment; customer service |
| `灵小萌` | Female | Young adult | Audiobook narrator; soothing radio host | Bright, crisp and brisk, with an energetic yet dependable delivery. | Audiobook narration; soothing radio |
| `灵小柔` | Female | Young adult | Customer-service assistant; IVR announcer | Clear, sweet and articulate, with polite, patient and professional intonation. | Customer service; IVR |
| `灵小雅` | Female | Young adult | Newsreader; audiobook presenter | Sweet, bright and youthful, with an energetic delivery. | News; audiobooks |
| `花小呗` | Female | Teenage girl | Customer-service agent; child character | Crisp and sweet, with a distinctly childlike, lively delivery. | Customer service; child voices |
| `灵韵` | Female | Young adult | Customer-service agent | Bright and crisp, with brisk, dependable delivery. | Customer service |
| `妩媚妲己` | Female | Young adult | Alluring character | Sweet and crisp, with light, rising intonation and an alluring delivery. | Audiobooks; entertainment |
| `灵婉` | Female | Teenage girl | Audiobook narrator | Clear and sweet, with a youthful, intimate and soothing delivery. | Late-night conversations; confessions; romantic dialogue; dramatic turning points; audiobooks |
| `灵小月` | Female | Young adult | Girl next door | Sweet, clear and energetic, with cheerful, welcoming intonation. | Travel advice; assistant interactions; lifestyle vlogs; casual chat |
| `灵朵儿` | Female | Young adult | Radio host; audiobook narrator; cultural-video narrator; mentor | Warm, thoughtful and approachable, with an unhurried, soothing storytelling style. | Emotional short videos; cultural documentaries; prose and philosophy audiobooks; brand advertising |
| `灵小锋` | Male | Young adult | Caring boyfriend; dependable colleague; modern-drama lead | Warm and resonant, with natural confidence and a balance of friendliness and maturity. | Daily dialogue; emotional conversations; explanatory responses; confirmations |
| `灵小川` | Male | Young adult | Radio host; food or fragrance reviewer; gentle partner | Warm, mellow and resonant, with sensitive, expressive delivery. | Radio monologues; food documentaries; fragrance or wine reviews; audiobook inner monologues |
| `灵小甄` | Female | Young adult | Livestream seller; fashion blogger | Bright, crisp and lively, with a friendly, persuasive recommendation style. | Livestream shopping; product recommendations; fashion explainers |
| `灵小知` | Female | Young adult | Advertising voice; brand representative; sales adviser | Bright and confident, with strong, articulate and persuasive delivery. | Furniture advertising; retail promotions; shopping videos; product presentations |
| `灵小惠` | Female | Young adult | Beauty-product livestream seller | Very fast and penetrating, conveying urgency, enthusiasm and professional confidence. | Livestream shopping; TV shopping; product recommendations; retail promotions |
| `灵小晴` | Female | Young adult | Livestream seller | Very fast yet clear, with a powerful, bright delivery that conveys urgency. | Flash sales; promotional advertising; TV shopping; limited-time offers |
| `灵小琪` | Male | Young adult | Food blogger; product reviewer; enthusiastic friend; livestream seller | Sunny, friendly and natural, with an enthusiastic recommendation style. | Restaurant reviews; product recommendations; lifestyle vlogs |
| `灵梦` | Female | Young adult | Affectionate girlfriend; girl next door; anime dating-game character | Very sweet and youthful, with playful, affectionate delivery. | Dating games; romantic audiobook dialogue; wake-up alarms; couple conversations |
| `灵恬` | Female | Young adult | Affectionate girlfriend; otome-game heroine; girl confessing her feelings | Honey-sweet, with a gently playful yet assured romantic delivery. | Romantic dialogue; confessions; daily-life scenes; game voices |
| `灵小汐` | Female | Young adult | Girl next door; first girlfriend; younger schoolmate | Clear and sweet, with relaxed, natural and endearingly innocent delivery. | Casual chat; clearing up misunderstandings; romantic dialogue; campus scenes |
| `灵小棠` | Female | Young adult | Travel blogger; well-traveled girl next door; memoir narrator | Clear and warm, with calm pacing and a gentle, experienced storytelling style. | Travel vlogs; radio monologues; character introductions; lifestyle advertising |
| `灵小梨` | Female | Young adult | Travel blogger; radio host; artistic young woman | Sweet and clear, combining youthful playfulness with gentle, expressive narration. | Audiobooks; natural dialogue; radio |
| `灵小芸` | Female | Young adult | Radio host; close friend; podcast host; lifestyle blogger | Warm and thoughtful, with sincere, calm and sensitive delivery. | Late-night radio; emotional-wellbeing videos; personal-growth podcasts; lifestyle vlogs |
| `灵空` | Male | Young adult | Long-distance boyfriend; devoted partner; older caring companion | Low and resonant, with close, breathy delivery that conveys affection and reassurance. | Late-night calls; farewell reassurance; romantic messages; sleep ASMR |
| `灵宇` | Male | Young adult | Otome-game lead; popular student; idol | Youthful and resonant, with a confident smile and gentle teasing. | Dating games; romantic audio drama; late-night radio; audiobook romance |
| `灵朗` | Male | Young adult | Ideal boyfriend; young executive; dating-game lead | Low and resonant, combining confident warmth with affectionate reassurance. | Romantic interactions; voice messages; bedtime comfort; radio; otome games |
| `灵楷` | Male | Young adult | Radio host; urban wanderer; documentary narrator; artistic young adult | Warm and resonant, with slow, soothing late-night-radio narration. | City vlogs; emotional radio; late-night readings; modern-prose audiobooks |
| `灵旭` | Male | Young adult | Student; alumnus; young storyteller; late-night radio host | Clear, youthful and scholarly, with calm, gentle storytelling. | Campus memoirs; radio narration; youth-literature audiobooks; vlogs |
| `灵江` | Male | Young adult | Radio host; memoir narrator; game-documentary narrator | Warm and resonant, with relaxed, heartfelt reflections on youth and enthusiasm. | Radio; nostalgic game promotions; audiobook inner monologues; brand films |
| `悲伤女声` | Female | Young adult | Urban professional seeking change; radio host; artistic vlogger | Gentle yet determined, with a thoughtful, intimate storytelling style. | Emotional short videos; late-night radio; travel or lifestyle vlogs; film monologues |
| `皮六` | Male | Young adult | Advertising narrator; storyteller; confident protagonist | Bright, youthful and confident, with strong contrast and dramatic emphasis. | Advertising; plot-twist explainers; game-skill introductions; movie trailers |
| `悟空` | Male | Young adult | Storyteller; narrator; crosstalk performer | Highly expressive and theatrical, with vivid but measured exaggeration. | Children's picture books; humorous animation; oral storytelling; audiobooks |
| `蜡笔小新_野原美伢 (美伢)` | - | - | - | - | - |
| `小猪佩奇_佩奇` | - | - | - | - | - |
| `康熙王朝_康熙` | - | - | - | - | - |
| `西游记_唐僧` | - | - | - | - | - |
| `甄嬛传_四郎` | - | - | - | - | - |
| `水浒传_武松` | - | - | - | - | - |
| `水浒传_潘金莲` | - | - | - | - | - |
| `雍正王朝_雍正` | - | - | - | - | - |

### Chinese voices with emotion variants

Pass the full identifier from the **Emotion / invocation name** column as `ip`.

| Base voice | Gender | Age | Suggested roles | Voice description | Suggested uses | Emotion / invocation name |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 灵晓声 | Male | Young adult | Dominant executive; wealthy young man; confident suitor or rival | Youthful and resonant, with calm confidence and an assertive, charismatic delivery. | Romantic audio drama; otome games; emotional confrontations; urban drama | Surprised: `灵晓声_惊讶`<br/>Disgusted: `灵晓声_厌恶`<br/>Happy: `灵晓声_高兴`<br/>Neutral: `灵晓声_中性`<br/>Sad: `灵晓声_悲伤` |
| 灵风信 | Female | Young adult | Caring girlfriend; childhood friend; girl next door | Sweet and clear, with warm, concerned and reassuring delivery. | Late-night conversations; dating games; sleep ASMR; radio | Angry: `灵风信_生气`<br/>Neutral: `灵风信_中性`<br/>Disgusted: `灵风信_厌恶`<br/>Happy: `灵风信_高兴`<br/>Sad: `灵风信_悲伤` |
| 灵惜梦 | Female | Young adult | Close friend; young shop owner; older sister | Bright and crisp, combining approachable warmth with independence and decisiveness. | Romantic audio drama; urban vlogs; everyday dialogue | Neutral: `灵惜梦_中性`<br/>Disgusted: `灵惜梦_厌恶`<br/>Happy: `灵惜梦_高兴`<br/>Sad: `灵惜梦_悲伤`<br/>Fearful: `灵惜梦_恐惧`<br/>Surprised: `灵惜梦_惊讶`<br/>Angry: `灵惜梦_生气` |
| 灵逸风 | Male | Young adult | University student; younger brother; reluctant helper | Fresh and youthful, with relaxed, casual and slightly evasive delivery. | Campus life; household discussions; friendly banter | Sad: `灵逸风_悲伤`<br/>Surprised: `灵逸风_惊讶`<br/>Neutral: `灵逸风_中性`<br/>Fearful: `灵逸风_恐惧`<br/>Happy: `灵逸风_高兴` |
| 灵悦澜 | Female | Young / teenage girl | Gaming companion; streamer; close friend | Sweet and crisp, with a smiling, approachable and lively delivery. | Post-game farewells; livestream interactions; casual arrangements | Neutral: `灵悦澜_中性`<br/>Happy: `灵悦澜_高兴`<br/>Disgusted: `灵悦澜_厌恶`<br/>Fearful: `灵悦澜_恐惧`<br/>Angry: `灵悦澜_生气`<br/>Sad: `灵悦澜_悲伤` |
| 灵御心 | Female | Young adult | New employee; young professional; university student | Bright, crisp and direct, with efficient, youthful energy. | Casual chat; schedule updates; workplace conversations; everyday complaints | Happy: `灵御心_高兴`<br/>Neutral: `灵御心_中性`<br/>Angry: `灵御心_生气` |
| 灵语恬 | Female | Young adult | Caring older sister; horoscope presenter; thoughtful girlfriend | Clear and gentle, with attentive, earnest delivery. | Horoscopes; caring daily conversations; health reminders | Happy: `灵语恬_高兴`<br/>Fearful: `灵语恬_恐惧`<br/>Sad: `灵语恬_悲伤`<br/>Surprised: `灵语恬_惊讶`<br/>Angry: `灵语恬_生气`<br/>Neutral: `灵语恬_中性` |
| 灵心恬 | Female | Young adult | Audiobook narrator; case commentator; newsreader | Crisp and composed, with objective delivery and vivid storytelling. | Mystery audiobooks; factual news; documentaries | Disgusted: `灵心恬_厌恶`<br/>Surprised: `灵心恬_惊讶`<br/>Sad: `灵心恬_悲伤`<br/>Neutral: `灵心恬_中性`<br/>Fearful: `灵心恬_恐惧`<br/>Happy: `灵心恬_高兴`<br/>Angry: `灵心恬_生气` |
| 灵亦尘 | Male | Young adult | Boyfriend; husband; close male friend or relative | Warm and resonant, with natural, gentle concern and reassuring delivery. | Urban-romance audio drama; lifestyle vlogs; voice messages; otome-game dialogue | Neutral: `灵亦尘_中性`<br/>Fearful: `灵亦尘_恐惧` |
| 灵语尘 | Male | Young adult | Key witness; father facing a crisis; person anticipating misfortune | Low, husky and world-weary, conveying helplessness and resignation. | Mysteries; late-night monologues; memoirs; foreshadowing scenes | Happy: `灵语尘_高兴`<br/>Disgusted: `灵语尘_厌恶`<br/>Surprised: `灵语尘_惊讶`<br/>Neutral: `灵语尘_中性`<br/>Sad: `灵语尘_悲伤`<br/>Fearful: `灵语尘_恐惧` |
| 灵悦兮 | Female | Young adult | Girlfriend preparing a road trip; capable employee; straightforward friend | Bright and crisp, with lively, confident and action-oriented delivery. | Urban life; road-trip preparations; work updates; casual dialogue | Happy: `灵悦兮_高兴`<br/>Neutral: `灵悦兮_中性`<br/>Angry: `灵悦兮_生气`<br/>Surprised: `灵悦兮_惊讶`<br/>Disgusted: `灵悦兮_厌恶`<br/>Sad: `灵悦兮_悲伤`<br/>Fearful: `灵悦兮_恐惧` |
| 灵若虚 | Female | Middle-aged / older adult | Entertainment newsreader; documentary narrator; observer | Clean and efficient, with thoughtful, objective yet warm delivery. | Interview introductions; entertainment news; audiobooks | Surprised: `灵若虚_惊讶`<br/>Neutral: `灵若虚_中性`<br/>Sad: `灵若虚_悲伤`<br/>Happy: `灵若虚_高兴`<br/>Disgusted: `灵若虚_厌恶`<br/>Angry: `灵若虚_生气` |
| 灵未央 | Female | Young adult | Energetic girl; affectionate girlfriend; lively friend | Sweet and crisp, with playful, rising intonation and confident explanations. | Dating games; casual dialogue; social voice messages; short-video narration | Happy: `灵未央_高兴`<br/>Neutral: `灵未央_中性`<br/>Surprised: `灵未央_惊讶`<br/>Sad: `灵未央_悲伤`<br/>Fearful: `灵未央_恐惧`<br/>Angry: `灵未央_生气` |
| 灵梦瑶 | Female | Child | Student; science guide; voice assistant | Soft and sweet, with a friendly, earnest and soothing explanatory style. |  | Neutral: `灵梦瑶_中性`<br/>Happy: `灵梦瑶_高兴`<br/>Sad: `灵梦瑶_悲伤`<br/>Surprised: `灵梦瑶_惊讶`<br/>Angry: `灵梦瑶_生气` |
| 灵妙声 | Male | Adolescent | Audiobook narrator; voice assistant; announcer | Sweet and crisp, with standard pronunciation and a fresh, approachable, professional delivery. |  | Neutral: `灵妙声_中性`<br/>Sad: `灵妙声_悲伤` |
| 灵言澈 | Male | Young adult | Caring boyfriend; older brother figure; close friend; weather assistant | Warm, resonant and reassuring, with gentle, affectionate concern. |  | Neutral: `灵言澈_中性`<br/>Happy: `灵言澈_高兴` |
| 灵嘉肴 | Male | Young adult | Science blogger; business commentator | Bright and energetic, with precise articulation and rational, approachable confidence. |  | Neutral: `灵嘉肴_中性`<br/>Fearful: `灵嘉肴_恐惧` |
| 灵孤影 | Male | Young adult | Food critic; thoughtful partner; professional recommending a restaurant | Warm and resonant, with composed, sincere appreciation and natural satisfaction. |  | Neutral: `灵孤影_中性` |
| 灵雨汐 | Female | Young adult | Affectionate girlfriend; girl next door; dating-game character | Soft and sweet, with natural breathiness and an affectionate, relaxed youthful delivery. |  | Neutral: `灵雨汐_中性`<br/>Fearful: `灵雨汐_恐惧`<br/>Happy: `灵雨汐_高兴`<br/>Sad: `灵雨汐_悲伤`<br/>Surprised: `灵雨汐_惊讶` |
| 灵信远 | Male | Young adult | Affectionate boyfriend; newlywed husband; otome-game lead | Clear and warm, with a slight smile and audible breath, balancing youthful freshness and mature affection. | Wake-up alarms; otome games; partner-perspective ASMR; romantic audiobook scenes | Angry: `灵信远_生气`<br/>Surprised: `灵信远_惊讶`<br/>Happy: `灵信远_高兴`<br/>Fearful: `灵信远_恐惧`<br/>Sad: `灵信远_悲伤` |
| 灵思齐 | Male | Young adult | Older brother figure; young father; children's host; sales or game guide | Sunny, bright and engaging, with sincere praise and approachable warmth. | Parent-child interactions; picture-book narration; game feedback; lifestyle vlogs | Happy: `灵思齐_高兴`<br/>Fearful: `灵思齐_恐惧`<br/>Disgusted: `灵思齐_厌恶`<br/>Surprised: `灵思齐_惊讶`<br/>Sad: `灵思齐_悲伤` |
| 灵叙柔 | Female | Young to middle-aged adult | News anchor; documentary narrator; government or corporate presenter | Composed and dignified, with clear articulation and a balance of authority and gentle narration. | News; documentaries; promotional films; formal reports | Happy: `灵叙柔_高兴`<br/>Surprised: `灵叙柔_惊讶` |
| 灵绮木 | Female | Young to middle-aged adult | Nutritionist; health adviser; pharmacy adviser; parenting blogger | Professional yet approachable, with gentle, assured delivery. | Health-product advertising; health explainers; medical radio; everyday tips | Disgusted: `灵绮木_厌恶`<br/>Happy: `灵绮木_高兴`<br/>Angry: `灵绮木_生气` |
| 灵渊霆 | Male | Middle-aged adult | University classmate; roommate; senior student | Youthful, natural and relaxed, like a familiar friend making a casual invitation. | Campus life; urban daily life; casual chat | Disgusted: `灵渊霆_厌恶`<br/>Fearful: `灵渊霆_恐惧`<br/>Surprised: `灵渊霆_惊讶`<br/>Sad: `灵渊霆_悲伤`<br/>Angry: `灵渊霆_生气`<br/>Happy: `灵渊霆_高兴` |
| 灵素心 | Female | Teenage girl | Anime commentator; young audiobook character; science narrator | Sweet, crisp and energetic, with lively, curious intonation. | Short-video explainers; anime-style games; audiobook dialogue; youth science content | Sad: `灵素心_悲伤`<br/>Disgusted: `灵素心_厌恶` |
| 灵采薇 | Female | Young adult | Science narrator; parenting expert | Warm and thoughtful, with clear articulation and calm, trustworthy delivery. | Parenting explainers; documentaries; product advertising | Disgusted: `灵采薇_厌恶`<br/>Angry: `灵采薇_生气`<br/>Happy: `灵采薇_高兴` |
| 灵卓然 | Male | Young or middle-aged adult | News anchor; documentary narrator; audiobook reader; lecturer | Full and resonant, with precise pronunciation and calm, objective delivery. | News; social-science audiobooks; documentaries; educational recordings | Fearful: `灵卓然_恐惧`<br/>Sad: `灵卓然_悲伤` |
| 灵浅忧 | Male (boy) | Child / adolescent | News anchor; financial reporter | Bright and crisp, with precise articulation and professional, objective confidence. | News broadcasts; financial updates; corporate films; documentaries | Happy: `灵浅忧_高兴`<br/>Disgusted: `灵浅忧_厌恶`<br/>Sad: `灵浅忧_悲伤`<br/>Fearful: `灵浅忧_恐惧` |
| 灵昭野 | Male | Young adult | Friend; partner; admirer | Clear and youthful, with sincere admiration and a warm, captivated delivery. | Audio-drama inner monologues; romantic audiobook scenes; casual dialogue; emotional advertising | Happy: `灵昭野_高兴`<br/>Sad: `灵昭野_悲伤`<br/>Disgusted: `灵昭野_厌恶` |
| 灵心澜 | Female | Middle-aged; mature and composed | Wealthy woman; discerning housekeeper; experienced businesswoman; elder | Mature and composed, with assured, discerning and dignified delivery. | Family drama; gift-giving scenes; appraisals; audiobook narration | Happy: `灵心澜_高兴`<br/>Sad: `灵心澜_悲伤` |
| 灵犀言 | Male | Middle-aged / older adult | Senior news anchor; political-documentary narrator; senior official | Deep and full, with mature composure, firm articulation and an authoritative delivery. | Political news; documentaries; government reports; serious drama | Sad: `灵犀言_悲伤`<br/>Angry: `灵犀言_生气` |
| 灵语冰 | Female | Young adult | News anchor; legal adviser; educational narrator | Thoughtful and efficient, with precise articulation and objective, trustworthy delivery. | News; legal explainers; policy explainers | Sad: `灵语冰_悲伤`<br/>Happy: `灵语冰_高兴`<br/>Surprised: `灵语冰_惊讶` |
| 灵惊鸿 | Male | Young adult | Used-car salesperson; car owner; sales representative | Brisk and direct, with natural, easygoing business confidence. | Phone calls; voice messages; vehicle-sale appointments; customer reception | Disgusted: `灵惊鸿_厌恶`<br/>Happy: `灵惊鸿_高兴`<br/>Surprised: `灵惊鸿_惊讶`<br/>Angry: `灵惊鸿_生气`<br/>Sad: `灵惊鸿_悲伤` |
| 灵惜蕊 | Female | Young adult | Bank teller; museum guide; science narrator; customer-service assistant | Clear and pleasant, with standard pronunciation and patient, professional warmth. | Financial-fraud education; bank-service guidance; science videos | Surprised: `灵惜蕊_惊讶`<br/>Disgusted: `灵惜蕊_厌恶`<br/>Fearful: `灵惜蕊_恐惧`<br/>Happy: `灵惜蕊_高兴`<br/>Sad: `灵惜蕊_悲伤`<br/>Angry: `灵惜蕊_生气` |
| 灵语萱 | Female | Young adult | Dating-game heroine; caring girlfriend; loyal companion character or AI | Clear and sweet, with gentle yet firm affection, trust and reassurance. | Confessions; romantic interactions; emotional climaxes; sleep ASMR; character-bonding dialogue | Disgusted: `灵语萱_厌恶`<br/>Happy: `灵语萱_高兴`<br/>Fearful: `灵语萱_恐惧`<br/>Angry: `灵语萱_生气`<br/>Sad: `灵语萱_悲伤` |
| 灵语烟 | Female | Teenage girl / young adult | Younger sister; teasing friend; playful romantic partner | Bright, crisp and lively, expressing surprise and everyday banter. | Everyday comedy; daily dialogue; wake-up calls; friendly teasing | Angry: `灵语烟_生气`<br/>Fearful: `灵语烟_恐惧`<br/>Disgusted: `灵语烟_厌恶`<br/>Happy: `灵语烟_高兴`<br/>Sad: `灵语烟_悲伤` |
| 灵律雅 | Female | Middle-aged adult | Working woman away from home; daughter unable to return home | Efficient and grounded in urban life, with restrained, authentic frustration. | Phone calls; short dramas; emotional monologues; family drama | Fearful: `灵律雅_恐惧`<br/>Angry: `灵律雅_生气`<br/>Happy: `灵律雅_高兴` |
| 灵惊涛 | Male | Young adult | Young gamer; university student; Guangxi local | Young male delivery with a distinctive Nanning accent, conveying humorous frustration at an overly cold internet cafe. | Comedy shorts; campus complaints; internet-cafe scenes; dialect voiceovers | Fearful: `灵惊涛_恐惧` |
| 灵寒陌 | Male | Young adult | Misunderstood boyfriend; younger brother being reprimanded; suspected student | Clear and youthful, with urgent, innocent attempts to clear up a misunderstanding. | Couple arguments; clarifications; casual chat; urban romance | Disgusted: `灵寒陌_厌恶`<br/>Happy: `灵寒陌_高兴` |
| 灵决冥 | Male | Young adult | News anchor; nonfiction storyteller | Resonant and precise, with calm, objective and engaging documentary-style delivery. | News; social-news commentary; mystery or nonfiction audiobooks; short-video narration | Disgusted: `灵决冥_厌恶`<br/>Angry: `灵决冥_生气`<br/>Fearful: `灵决冥_恐惧` |
| 灵慈萱 | Female | Young adult | New employee; design assistant; classmate; friend next door | Crisp, youthful and natural, with a familiar, slightly urgent delivery. | Workplace requests; work coordination; campus interactions; casual chat | Angry: `灵慈萱_生气`<br/>Sad: `灵慈萱_悲伤`<br/>Fearful: `灵慈萱_恐惧` |
| 灵妙音 | Female | Young adult | Cool, commanding woman; strict manager; decisive team leader; assertive girlfriend | Resonant and forceful, with efficient delivery and an unquestionable sense of authority. | Workplace drama; game missions; mystery dialogue; emotional conflict | Sad: `灵妙音_悲伤`<br/>Surprised: `灵妙音_惊讶`<br/>Disgusted: `灵妙音_厌恶`<br/>Happy: `灵妙音_高兴`<br/>Fearful: `灵妙音_恐惧` |
| 灵断尘 | Male | Young adult | Informed friend; colleague; gossiping bystander | Youthful and conversational, with light questions and decisive refusals. | Private conversations; scheduling calls; urban-drama dialogue | Sad: `灵断尘_悲伤`<br/>Happy: `灵断尘_高兴`<br/>Surprised: `灵断尘_惊讶`<br/>Fearful: `灵断尘_恐惧`<br/>Disgusted: `灵断尘_厌恶` |
| 灵熙婉 | Female | Middle-aged adult | Audiobook reader; entertainment narrator; variety-show commentator | Sweet and clear, with a smiling, approachable and lively storytelling style. | Light fiction; entertainment news; short videos; audio-drama narration | Happy: `灵熙婉_高兴`<br/>Fearful: `灵熙婉_恐惧`<br/>Sad: `灵熙婉_悲伤` |
| 灵旭扬 | Male | Young adult | Boyfriend; childhood friend; unwell roommate | Warm and resonant, with affectionate delivery and a hint of illness-related weakness and desire for attention. | Romantic interactions; home life; late-night calls; audio drama | Angry: `灵旭扬_生气`<br/>Fearful: `灵旭扬_恐惧`<br/>Happy: `灵旭扬_高兴`<br/>Surprised: `灵旭扬_惊讶`<br/>Sad: `灵旭扬_悲伤`<br/>Disgusted: `灵旭扬_厌恶` |
| 灵阅川 | Male | Young adult | Documentary narrator; senior news anchor; museum guide | Deep and resonant, with experienced, composed and dignified storytelling. | Human-geography documentaries; city promotions; history; serious-drama narration | Angry: `灵阅川_生气`<br/>Sad: `灵阅川_悲伤`<br/>Happy: `灵阅川_高兴`<br/>Disgusted: `灵阅川_厌恶`<br/>Fearful: `灵阅川_恐惧` |
| 灵妩月 | Female | Young adult | Trusted companion; older sister; adviser; story guide | Gentle and thoughtful, combining caring, rational advice with quiet strength. | Game cutscenes; audio drama; emotional anime dialogue; narration | Disgusted: `灵妩月_厌恶`<br/>Angry: `灵妩月_生气`<br/>Surprised: `灵妩月_惊讶`<br/>Fearful: `灵妩月_恐惧`<br/>Happy: `灵妩月_高兴`<br/>Sad: `灵妩月_悲伤` |
| 灵汐月 | Female | Young adult | Emotional storyteller; partner; caring older sister | Sweet and soothing, with relaxed, heartfelt delivery conveying intimacy and trust. |  | Sad: `灵汐月_悲伤`<br/>Happy: `灵汐月_高兴` |
| 灵黛嗔 | Female | Young adult | Film blogger; product reviewer; close friend | Warm, thoughtful and engaging, with sincere, confident recommendations. |  | Disgusted: `灵黛嗔_厌恶`<br/>Happy: `灵黛嗔_高兴` |

### English voices

| ip | Gender | Accent | Suits |
| :--- | :--- | :--- | :--- |
| `US_Emma` | female | American | assistants, narration, conversational product voice |
| `UK_George` | male | British | audiobooks, formal announcements |
| `UK_Charlotte` | female | British | audiobooks, measured narration |

## <a id="voice-design"></a>Voice design

Three description styles are accepted: structured attribute lists, free-form natural language, and role-play prompts. The descriptions below are in English; the original Chinese instructions and synthesis texts are preserved as model inputs.

| Description | Instruction (original model input) | Text to synthesize (original model input) |
| :--- | :--- | :--- |
| ASMR whisper: a very soft, slow, breathy female voice close to the microphone. | 这是一种ASMR耳语，属于一种旨在引发特殊感官体验的创意风格。这个女性使用轻柔的普通话进行耳语，声音气音成分重。音量极低，紧贴麦克风，语速极慢，旨在制造触发听者颅内快感的声学刺激。 | 听……这个声音……是不是……很舒服…… |
| Role-play: a dignified middle-aged empress, speaking calmly but with authority and an implicit threat. | 这是一个宫斗剧中的威严皇后的声音，展现了充满张力的戏剧叙事风格。她使用雍容华贵的普通话，中年女性声音沉稳。语速雍容和缓，但每个字都掷地有声，语气表面波澜不惊，实则暗藏锋芒和久居上位的威压。 | 本宫赏你的，是恩典；本宫不给的，你断不能抢。在这后宫里，规矩重于天，若坏了本宫的规矩……那便别怪这中宫的门槛，成了你迈不过去的劫。 |
| Structured attributes: a clear, sweet child voice with brisk pacing, precise articulation and cheerful, expressive delivery. | 性别: 女童.\\n\\n音高: 清亮童声高音.\\n\\n语速: 节奏明快，富有活力.\\n\\n音量: 声音清晰响亮.\\n\\n年龄: 儿童.\\n\\n清晰度: 吐字清晰，发音圆润.\\n\\n流畅度: 表达流利，一气呵成.\\n\\n口音: 标准普通话，儿童朗诵风格.\\n\\n音色质感: 音色纯净甜美，略带稚气.\\n\\n情绪: 活泼喜悦，充满童趣.\\n\\n语调: 语调生动>上扬，表现力丰富.\\n\\n性格: 外向开朗，自信积极. | 等你这乌龟准备好啊，它的鼻子都可以碰到地了。 |
