from manim import *
from manim.utils.file_ops import add_extension_if_not_present
from pathlib import Path
import os


class CoolXAnimation(Scene):
    def construct(self):
        # Load the image
        img_path = "static/image/logo.png"  # Update this to the path of your image
        logo1 = ImageMobject(img_path).scale(0.5)
        logo2 = ImageMobject(img_path).scale(0.5)

        # Set initial positions
        logo1.move_to(LEFT * 2)
        logo2.move_to(RIGHT * 2)

        # Animation to move images into the X formation
        self.play(logo1.animate.move_to(LEFT + UP), logo2.animate.move_to(RIGHT + DOWN))
        self.play(logo1.animate.move_to(RIGHT + UP), logo2.animate.move_to(LEFT + DOWN))

        # Rotate images to form an X
        self.play(Rotate(logo1, angle=PI / 4), Rotate(logo2, angle=-PI / 4))

        # Final alignment in the center
        self.play(logo1.animate.move_to(UP * 0.5), logo2.animate.move_to(DOWN * 0.5))

        # Keep the final frame for a while
        self.wait(2)


if __name__ == "__main__":
    # Render the scene
    scene = CoolXAnimation()
    scene.render()

    # Convert the output to GIF
    output_file = Path(scene.renderer.file_writer.movie_file_path)
    gif_file = add_extension_if_not_present(output_file, ".gif")

    os.system(f"ffmpeg -i {output_file} {gif_file}")

    # Move the GIF to the gifs folder
    gifs_folder = Path("static/gifs")
    gifs_folder.mkdir(exist_ok=True)
    gif_file.rename(gifs_folder / gif_file.name)
