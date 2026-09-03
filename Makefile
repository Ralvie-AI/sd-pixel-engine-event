build:
	poetry install

package:
	pyinstaller sd-pixel-engine-event.spec --clean --noconfirm

clean:
	rm -rf build dist
	rm -rf sd_pixel_engine_event/__pycache__

