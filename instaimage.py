# PROJECT TO GET IMAGES RELEVANT TO INSTAGRAM
# TAKE A SCREENSHOT OF AMIBROKER IMAGE
# RUN THE PROGRAM,
# GIVE A TITLE to be written by program on the IMAGE,
# GIVE A SUBJECT to be written at the bottom of the page
from PIL import Image, ImageDraw, ImageFont, PSDraw, ImageGrab
import os

target_size = [(1080, 1100), (1350, 1080), (1080, 608)]
temp_centre_image = './tempimage.png'
color_dict = {'black':{'hash':'000000','rgb':'rgb(0,0,0)'}, 'white':{'hash':'#ffffff','rgb':'rgb(255, 255, 255)'},
              'blue1':{'hash':'#21A1E1', 'rgb':'rgb(33,161,225)'}, 'blue2':{'hash':'#5DB7D2','rgb':'rgb(93,183,210)'},
              'blue3':{'hash':'#00A3FE','rgb':'rgb(0,163,254)'},'green1':{'hash':'#00F954','rgb':'rgb(0,249,84)'},
              'yellow1':{'hash':'#FFFF01','rgb':'rgb(255,255,1)'},'yellow2':{'hash':'#FFFE57','rgb':'rgb(255,254,87)'},
              'red1':{'hash':'#CC0118','rgb':'rgb(204,1,24)'},
              }

# insta_blue = #21A1E1  rgb(33,161,225)
#insta_blue1   #5DB7D2      rgb(93,183,210)
# instablue1   #00A3FE         rgb(0,163,254)
# insta green = #00F954     rgb(0,249,84)
# insta_yellow1 = #FFFF01           #rgb(255,255,1)
#insta_yellow = #FFFE57      rgb(255,254,87)
#insta red = #CC0118           rgb(204,1,24)
# takes the image and resizes, saves in same image

def resize(resize_path, target_size,resized_path):
    # Open the image
    image = Image.open(resize_path)
    # Resize the image to the target size while maintaining aspect ratio
    #image.thumbnail(target_size)
    new_image = image.resize(target_size)
    new_image.save(resized_path)

def box_text(image,text,font,color,box_color):              # send an image only
    draw = ImageDraw.Draw(image)
    # Center-align text
    title_width, title_height = draw.textsize(text, font=font)
    # Create black bars on top
    draw.rectangle((0, 0, image.width, title_height), fill=box_color)

    # Calculate the position for the title and subject text
    title_position = (image.width // 2, title_height // 2)
    print(image.height)
    print(title_height)
    print(title_height//2)
    title_position = ( title_position[0] - title_width // 2, -5)#title_position[1] - title_height // 2)
    # Draw the title and subject text on the image
    draw.text(title_position, text, fill=color, font=font)

    #title_x = (image.width - title_width) // 2
    #title_y = (image.height - title_height) // 2
    # Draw the title text at the centered position
    #draw.text((title_x, title_y), text, fill=color, font=font)

    return title_height

def wrap_draw_text(image,text,font,color,box_color):
    draw = ImageDraw.Draw(image)
    add_lines = ""
    tot_box_height = 0
    wrapped_text = []
    for each in text.split(' '):
        text_width, text_height = draw.textsize(add_lines + each.upper() + " ", font=font)
        #print(each)
        if each == '\\n':
            tot_box_height += text_height
            wrapped_text.append(add_lines)
            add_lines = ""
            print(f"Wrapped text {wrapped_text} and starting new one from {add_lines}")

        elif text_width > image.width:
            tot_box_height += text_height
            wrapped_text.append(add_lines)
            add_lines = each + " "
            print(f"Wrapped text {wrapped_text} and starting new one from {add_lines}")
        else:
            add_lines += each + " "

    tot_box_height += text_height
    wrapped_text.append(add_lines)
    print(wrapped_text)
    #print(tot_box_height)
    # Calculate the height for the text
    draw.rectangle((0, image.height - tot_box_height, image.width, image.height), fill=box_color)
    # Adjust the subject box height if necessary
    subject_position = (image.width // 2, (image.height - tot_box_height // 2) -5)
    # Calculate the initial Y position for subject text within the bottom box
    current_y = subject_position[1] - (tot_box_height // 2)
    # Draw each line of the subject text within the bottom box
    for each_line in wrapped_text:
        #print(each_line)
        line_width, line_height = draw.textsize(each_line, font=font)
        line_position = ( subject_position[0] - line_width // 2, current_y)
        draw.text(line_position, each_line, fill=color, font=font)
        current_y += line_height
        print(f"WRITTEN {each_line}")
    return tot_box_height

def multiline_image(final_image_width,text, font, color, box_color):
    bg_color = (0, 0, 0)  # Black color
    # Plain BLACK image on top of which work shall be carried out
    image = Image.new("RGB", target_size[0], bg_color)
    draw = ImageDraw.Draw(image)
    draw = ImageDraw.Draw(image)
    add_lines = ""
    tot_box_height = 0
    wrapped_text = []
    for each in text.split(' '):
        text_width, text_height = draw.textsize(add_lines + each + " ", font=font)
        if text_width < image.width:
            add_lines += each + " "
        else:
            tot_box_height += text_height
            wrapped_text.append(add_lines)
            add_lines = each + " "
    tot_box_height += text_height
    wrapped_text.append(add_lines)
    #print(wrapped_text)
    print(tot_box_height)
    # Calculate the height for the text
    draw.rectangle((0, image.height - tot_box_height, image.width, image.height), fill=box_color)

    # Adjust the subject box height if necessary
    subject_position = (image.width // 2, image.height - tot_box_height // 2)
    # Calculate the initial Y position for subject text within the bottom box
    current_y = subject_position[1] - (tot_box_height // 2)
    # Draw each line of the subject text within the bottom box
    for each_line in wrapped_text:
        print(each_line)
        line_width, line_height = draw.textsize(each_line, font=font)
        line_position = (subject_position[0] - line_width // 2, current_y)
        draw.text(line_position, each_line, fill=color, font=font)
        current_y += line_height
        print(f"WRITTEN {each_line}")



def create_image(centre_image, title_text, title_font, title_color, title_box_color, subject_text, subject_font, subject_color, subject_box_color, output_path):
    # Define colors for the black bars
    bg_color = color_dict['black']['rgb']
    image_size = target_size[0]
    # Plain BLACK image on top of which work shall be carried out
    image = Image.new("RGB", image_size, bg_color)
    draw = ImageDraw.Draw(image)
    # Get the dimensions of the image
    width, height = image.size

    #A1 Define fonts and colors for title
    title_height = box_text(image,title_text,title_font,title_color,title_box_color)
    #title_height = wrap_draw_text(image,title_text,title_font,title_color,bg_color)

    # B1
    # Define fonts and colors for subject
    #Get a LIST[ of lines fitting the IMAGE width ] and dimensions(no_of_lines for whole_text)
    subject_height = wrap_draw_text(image, subject_text, subject_font,subject_color,subject_box_color)

    # first resize the middle PIC to a size that fits within the BOXES
    resize(centre_image,(image_size[0],(image_size[1]-title_height - subject_height)),output_path)             # pass an opened image, not filepath
    temp_image = Image.open(output_path)
    image.paste(temp_image,(0,title_height))
    image.save(output_path)

def create_instaimage(title_text,subject_text,image_path):
    savenameas = os.path.basename(image_path)
    output_path = "./insta/" + savenameas + ".png"  # Replace with the desired output path
    # output_path = "C:/Users/sahaveer/OneDrive/Documents/bhavcopy/" + title_text + ".png"

    bg_color = color_dict['black']['rgb']
    title_color = bg_color
    title_box_color = color_dict['blue1']['rgb']
    title_font = ImageFont.truetype("arial.ttf", size=44)
    subject_font = ImageFont.truetype("arial.ttf", size=42)
    subject_box_color = bg_color
    subject_color = title_box_color

    follow_me = "@itimesalgo"
    # centre_image = './insta.png'
    screenshot_image = ImageGrab.grabclipboard()

    if isinstance(screenshot_image, Image.Image):
        centre_image = './insta/Ainstagram.png'
        image_at_centre = screenshot_image.save(centre_image)
    else:
        centre_image = image_path

    create_image(centre_image, title_text.upper(), title_font, title_color, title_box_color, subject_text,
                 subject_font, subject_color, subject_box_color,
                 output_path)  # send the path of Centre image not the Image itself
    Image.open(output_path).show()


if __name__ == "__main__":
    print("Give a title")
    title_text = input()
    #subject_text = "Accumulate at 300 and very gud stock to buy at times wen index is totally down to dynamic supports"
    print("Input subject now")
    subject_text = input()
    output_path = "./insta/" + title_text + ".png" # Replace with the desired output path
    output_path = "C:/Users/sahaveer/OneDrive/Documents/bhavcopy/" + title_text + ".png"

    bg_color = color_dict['black']['rgb']
    title_color = bg_color
    title_box_color = color_dict['blue1']['rgb']
    title_font = ImageFont.truetype("arial.ttf", size=96)
    subject_font = ImageFont.truetype("arial.ttf", size=42)
    subject_box_color = bg_color
    subject_color = title_box_color

    follow_me = "@itimesalgo"
    #centre_image = './insta.png'
    screenshot_image = ImageGrab.grabclipboard()
    if isinstance(screenshot_image, Image.Image):
        centre_image = './insta/Ainstagram.png'
        image_at_centre = screenshot_image.save(centre_image)
        #print(f"Screenshot image size is {screenshot_image.size}")
        create_image(centre_image, title_text.upper(), title_font, title_color, title_box_color, subject_text, subject_font, subject_color, subject_box_color, output_path)            # send the path of Centre image not the Image itself
        Image.open(output_path).show()
    else:
        print("Cannot find any image in the clipboard")