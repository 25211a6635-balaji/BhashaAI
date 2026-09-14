import ctranslate2
from transformers import NllbTokenizer


# VAK model location
model_path = r"C:\Users\balaj\.cache\huggingface\hub\models--shunyalabs--vak-translate-1.3b-ct2\snapshots\ca40bc46f5ecd1f8b71566f0474bd8c745c892de"


print("==========================================")
print("       BHASHAAI VAK TRANSLATION TEST")
print("==========================================")

print()
print("Loading tokenizer...")

tokenizer = NllbTokenizer.from_pretrained(
    model_path
)

print("Tokenizer loaded successfully! ✅")

print()
print("Loading VAK translation model...")
print("This may take some time...")

translator = ctranslate2.Translator(
    model_path,
    device="cpu"
)

print("VAK model loaded successfully! ✅")


# ------------------------------------------------
# Test 1: Hindi → Hindi
# ------------------------------------------------

sentence = "तुम कहाँ जा रहे हो"

source_language = "hin_Deva"
target_language = "hin_Deva"

print()
print("==========================================")
print("              TEST 1")
print("==========================================")

print("Input:", sentence)
print("Source language:", source_language)
print("Target language:", target_language)

# Tell tokenizer what language the input is
tokenizer.src_lang = source_language

# Convert sentence into model tokens
inputs = tokenizer(sentence)

source_tokens = tokenizer.convert_ids_to_tokens(
    inputs["input_ids"]
)

print()
print("Translating...")

results = translator.translate_batch(
    [source_tokens],
    target_prefix=[[target_language]],
    beam_size=4,
    max_decoding_length=256
)

output_tokens = results[0].hypotheses[0]

output_ids = tokenizer.convert_tokens_to_ids(
    output_tokens
)

translation = tokenizer.decode(
    output_ids,
    skip_special_tokens=True
)

print()
print("AI Output:", translation)


# ------------------------------------------------
# Test 2: English → Hindi
# ------------------------------------------------

sentence2 = "Hello, how are you?"

source_language2 = "eng_Latn"
target_language2 = "hin_Deva"

print()
print("==========================================")
print("              TEST 2")
print("==========================================")

print("Input:", sentence2)
print("Source language:", source_language2)
print("Target language:", target_language2)

tokenizer.src_lang = source_language2

inputs2 = tokenizer(sentence2)

source_tokens2 = tokenizer.convert_ids_to_tokens(
    inputs2["input_ids"]
)

print()
print("Translating...")

results2 = translator.translate_batch(
    [source_tokens2],
    target_prefix=[[target_language2]],
    beam_size=4,
    max_decoding_length=256
)

output_tokens2 = results2[0].hypotheses[0]

output_ids2 = tokenizer.convert_tokens_to_ids(
    output_tokens2
)

translation2 = tokenizer.decode(
    output_ids2,
    skip_special_tokens=True
)

print()
print("AI Output:", translation2)


print()
print("==========================================")
print("              TEST COMPLETE")
print("==========================================")