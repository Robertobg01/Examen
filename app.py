from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Aqui configuramos la APIkey
api_key = "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"

class ImageDescriptionGenerator:
    def __init__(self):
        openai.api_key = api_key

    def generate_description(self, description):
        # Genera una descripción para la imagen usando ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates image descriptions."},
                {"role": "user", "content": f"Genera una descripción para una imagen: {description}"},
            ],
        )

        # Obtiene el texto generado desde la respuesta
        generated_description = response['choices'][0]['message']['content']
        return generated_description

    def generate_images(self, description, num_images):
        # Llama a la función para crear imágenes con DALL-E
        # (asegúrate de que la clave de API tenga acceso a DALL-E)
        image_urls = []
        for _ in range(num_images):
            response = openai.Image.create(
                prompt=description,
                n=1,  # Generar una imagen a la vez
                size='512x512'
            )
            image_urls.append(response["data"][0]["url"])
        return image_urls

image_description_generator = ImageDescriptionGenerator()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.json
        description = data["descripcion"]
        num_images = int(data["numeroImagenes"])
        try:
            generated_description = image_description_generator.generate_description(description)
            images = image_description_generator.generate_images(generated_description, num_images)
            return jsonify({"descripcion_generada": generated_description, "imagenes": images})
        except openai.error.APIError as e:
            return jsonify({"error": str(e)})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
