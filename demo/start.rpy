define test_character_1 = Character("test character 1")
define test_character_2 = Character("test character 2")

label start:
    "This is a demo of Twine to Ren'Py."
    
    jump go_to_the_next_passage

label go_to_the_next_passage:
    "Here's a sample of a Twine set of choices that can be converted to a Ren'Py menu with this tool."
    
    menu:
        "Go to option 1":
            jump go_to_option_1
        "Go to option 2":
            jump go_to_option_2

label go_to_option_1:
    test_character_1 "This is option 1!"
    
    jump continue_to_demo

label go_to_option_2:
    test_character_2 "This is option 2"
    
    jump continue_to_demo

label continue_to_demo:
    "Here's how to use a doc break tag to end a Ren'Py file."
    
    jump this_next_passage_will_now_be_a_new_file

