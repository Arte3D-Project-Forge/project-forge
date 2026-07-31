import os
import io

from datetime import datetime
from PIL import Image, ImageDraw

from app.ai.providers.images.image_provider import ImageProvider


class MockImageProvider(ImageProvider):

    def generate(
        self,
        prompt,
        filename,
        output_path
    ):
        try:
            os.makedirs(output_path, exist_ok=True)

            img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            seed = abs(hash(prompt + filename)) % 10
            colors = [
                (255, 100, 100),
                (100, 255, 100),
                (100, 100, 255),
                (255, 255, 100),
                (255, 100, 255),
                (100, 255, 255),
                (200, 150, 100),
                (150, 200, 100),
                (100, 150, 200),
                (200, 100, 150),
            ]
            color = colors[seed]

            draw.rectangle(
                [64, 64, 448, 448],
                fill=color,
                outline=(255, 255, 255),
                width=4
            )

            draw.ellipse(
                [128, 128, 192, 192],
                fill=(255, 255, 255)
            )
            draw.ellipse(
                [320, 128, 384, 192],
                fill=(255, 255, 255)
            )

            draw.rectangle(
                [192, 320, 320, 384],
                fill=(255, 255, 255)
            )

            file_path = os.path.join(
                output_path, filename + ".png"
            )

            img.save(file_path, "PNG")

            return {
                "status": "generated",
                "provider": "mock",
                "file": file_path,
                "size": os.path.getsize(file_path),
                "created_at":
                    datetime.now().isoformat()
            }

        except Exception as error:
            return {
                "status": "error",
                "provider": "mock",
                "message": str(error)
            }
