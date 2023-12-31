from pathlib import Path
import face_recognition
import pickle
from collections import Counter
from PIL import Image, ImageDraw
import sys
import time

# import lib/myUtils as util
# config 

print("="*10, "Face Labeler","="*10)
DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")
BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"

def recognize_faces(
    image_location: str,
    output_location:str,
    model: str = "cnn",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
        
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)

    input_face_locations = face_recognition.face_locations(
      input_image, model=model
    )
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )

    # For drawing bounding over image
    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)

    detected_faces = []
    # Finding Multiple faces in the image
    t1 = time.time()
    for bounding_box, unknown_encoding in zip(
    input_face_locations, input_face_encodings
    ):
        name = _recognize_face(unknown_encoding, loaded_encodings)

        if(name != "unknown"):
            if(name in detected_faces):
                name = "unknown"
            else:
                detected_faces.append(name)
        
        # tt = ("%.4f" % ((t2-t1)))
        # print(f"\n{name} : {((t2 - t1)*1000)}ms")
        if not name:
            name = "Unknown"
        # print(name, bounding_box)
        _display_face(draw, bounding_box, name, name == "abhay" if "red" else "blue")
    
    t2 = time.time()
    print(f"Face detected in {((t2 - t1)*1000)} ms !")
    del draw
    pillow_image.save(output_location)
    print("Result image saved in test/known.jpg")
    # pillow_image.show()

def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    # print("")
    # names = loaded_encodings['names']
    # print(f"boolean_matches : \n{boolean_matches}\n{names}")
    # for i in range(len(names)):
    #     if(boolean_matches[i]):
    #         print(names[i], end=" ")

    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def _display_face(draw, bounding_box, name, clr=BOUNDING_BOX_COLOR):
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=clr)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill=clr,
        outline=clr,
    )
    draw.text(
        (text_left, text_top),
        name,
        fill="white",
    )

if(len(sys.argv) >= 3) :
    source = sys.argv[1]
    output = sys.argv[2]
    print(f"source : {source} , output : {output}")
    recognize_faces(source, output)
else :
    print("Error : not enough arguments !")