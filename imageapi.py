import torch
import clip
from transformers import BigGANConfig, BigGANModel, BigGANForConditionalGeneration, BigGANTokenizer

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)

# Load the BigGAN model and tokenizer
biggan_config = BigGANConfig.from_pretrained("biggan-deep-128")
biggan_model = BigGANForConditionalGeneration.from_pretrained("biggan-deep-128")
biggan_tokenizer = BigGANTokenizer.from_pretrained("biggan-deep-128")

# Set the maximum length for the text prompt
max_length = 32

# Text prompt
prompt = "a cat sitting on a table"

# Encode the text prompt using CLIP
with torch.no_grad():
    text_tokens = clip_preprocess([prompt]).to(device)
    text_features = clip_model.encode_text(text_tokens)

# Generate image features from the text features using BigGAN
with torch.no_grad():
    image_features = biggan_model.generate_image_from_text(text_features)

# Decode the image features into an image
image = biggan_model.generate_image(image_features)

# Display the generated image
image.show()
