label this_next_passage_will_now_be_a_new_file:
    "Here's an example of using passage transitions with differing text from the passage titles. In Ren'Py a menu with the text choice will be shown and the label/jump statement will use the hidden passage name."
    
    menu:
        "Choice text 1":
            jump choice_1
        "Choice text 2":
            jump choice_2

label choice_1:
    "This is choice 1. We can even use this to go back to passages."
    
    menu:
        "Go back.":
            jump this_next_passage_will_now_be_a_new_file
        "Or continue on.":
            jump or_continue_on

label choice_2:
    "This is choice 2. We can even use this to go back to passages."
    
    menu:
        "Go back.":
            jump this_next_passage_will_now_be_a_new_file
        "Or continue on.":
            jump or_continue_on

label or_continue_on:
    "Let's test variables!"
    
    "What's your favorite color?"
    
    menu:
        "Red":
            jump red
        "Green":
            jump green
        "Blue":
            jump blue

label red:
    $ favorite_color = "red"
    
    jump variables_result

label green:
    $ favorite_color = "green"
    
    jump variables_result

label blue:
    $ favorite_color = "blue"
    
    jump variables_result

label variables_result:
    if favorite_color == "red":
        "Red? That is a cool color!"
    elif favorite_color == "blue":
        "Blue? That is my favorite color too!"
    else:
        "Green? That is so pretty!"
    
    jump now_to_the_end_of_the_demo

label now_to_the_end_of_the_demo:
    "That's the end of the demo!"
    
    jump end

label end:
    pass

