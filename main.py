from rembg import remove
from PIL import Image as PILImage  # Alias to avoid naming conflict
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.image import Image  # Image class from Kivy
import os

class RemoveBackgroundApp(App):
    def build(self):
        # Main layout structure
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Add a label
        self.label = Label(text="Choose an image to remove the background", size_hint=(1, 0.2))
        layout.add_widget(self.label)

        # "Image" button
        button = Button(text="Image", size_hint=(1, 0.4))
        button.bind(on_press=self.open_filechooser)
        layout.add_widget(button)

        return layout

    def open_filechooser(self, instance):
        # Create the file chooser window
        filechooser_layout = BoxLayout(orientation='vertical', spacing=10)

        # Add the FileChooser
        filechooser = FileChooserIconView()
        filechooser.filters = ['*.png', '*.jpg', '*.jpeg']
        filechooser_layout.add_widget(filechooser)

        # Add buttons to the window
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        select_button = Button(text="Select")
        cancel_button = Button(text="Cancel")
        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)

        filechooser_layout.add_widget(button_layout)

        # Create Popup
        popup = Popup(title="Select File", content=filechooser_layout, size_hint=(0.9, 0.9))
        popup.open()

        # Handle file selection
        def on_select(instance):
            if filechooser.selection:
                selected_file = filechooser.selection[0]
                self.label.text = f"Selected: {os.path.basename(selected_file)}"
                popup.dismiss()
                self.process_image(selected_file)  # Process the image

        select_button.bind(on_press=on_select)
        cancel_button.bind(on_press=lambda x: popup.dismiss())

    def process_image(self, image_path):
        try:
            output_path = 'output.png'
            with PILImage.open(image_path) as input_image:  # Using the alias PILImage
                input_image = input_image.convert("RGBA")
                output_image = remove(input_image)
                output_image.save(output_path)
            self.label.text = "Image processed successfully!"
        except Exception as e:
            self.label.text = f"Error: {e}"
            print(f"Error processing image: {e}")

if __name__ == "__main__":
    RemoveBackgroundApp().run()
