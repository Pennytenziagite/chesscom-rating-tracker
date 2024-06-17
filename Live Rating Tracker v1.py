from chessdotcom import get_player_stats, Client
import time
import matplotlib.pyplot as plt
import numpy as np

#This program is a standard rating tracker to aid with stuff like Tim TV, made by pennytenziagite. Enjoy!

#Settings

rating_list_length = 481 #Determines how many checks of rating are stored at once

wait_time = 15.0 #How long it waits between checks of tim's rating in seconds
pause_time = 2.0 #Increase this if the graphs aren't drawing properly (must be less than wait_time)

#Note the total time described will be (waiting_list_length - 1) * wait_time, by default 7200 seconds, or 2 hours
#                                                           ^ bc of the fencepost thingy

target_user = "timcannon25" #Can be changed for other tv's
target_user_name = "Tim"
TV_title = "Tim TV Test"

tv_format = "chess_blitz" #Can be changed to chess_bullet, chess_blitz, or chess_rapid

window_width = 14  #For some godforsaken reason these are in inches, I hate python
window_height = 10



#Setup

Client.request_config["headers"]["User-Agent"] = ( #This is all off-the-shelf API stuff
   "timtv test"
   "timtv"
)
response = get_player_stats(target_user)

user_rating = response.json["stats"][tv_format]["last"]["rating"]

min_rating = user_rating
max_rating = user_rating

rating_list = [user_rating] * rating_list_length  #Makes an initial rating setup for Tim



plt.ion() #Makes the plot using off-the-shelf matplotlib stuff

plt.style.use('bmh') #You can change the style by using other settings available in the pyplot docs

fig = plt.figure()
ax = fig.add_subplot()

fig.set_size_inches(window_width, window_height)

stair_plot = ax.stairs(rating_list, linewidth=2.5) 

ax.set(xlim=(1, rating_list_length-1),
        ylim=(min_rating-10, max_rating+10), yticks=np.arange(min_rating-10, max_rating+10, 5), 
        xlabel="Time", ylabel=target_user_name + "'s Rating",
        title=TV_title)


#Main loop

first_run = True #For some reason the settings aren't realised until the second time we draw the plot so this is just a quick and dirty solution \_:)_/

while True: 
    
    start = time.time() #The time.time stuff is here because the drawing takes up a non-trivial amount of time which needs to be accounted for

    fig.canvas.flush_events() #Used for updating the graph
    


    Client.request_config["headers"]["User-Agent"] = ( #API stuff again
       "timtv test "
       "timtv"
    )
    response = get_player_stats(target_user)

    user_rating = response.json["stats"][tv_format]["last"]["rating"] #Gets tim's current rating

    last_rating = rating_list[-1]
    
    rating_list = rating_list[1:] + [user_rating] #Updates the rating_list

    min_rating = min(rating_list) #There's probably a better way but can't be arsed tbh
    max_rating = max(rating_list)



    stair_plot.set_data(values=rating_list)

    fig.tight_layout() #Need this to put everything onscreen

    plt.xticks([]) #Makes the x-axis blank

    ax.set(xlim=(1, rating_list_length-1),
        ylim=(min_rating-10, max_rating+10), yticks=np.arange(min_rating-10, max_rating+10, 5),
        xlabel="Time", ylabel=target_user_name + "'s Rating",
        title=TV_title)

    fig.canvas.draw_idle()

    

    end = time.time()

    if first_run:
        first_run = False
    else:
        time.sleep(wait_time - end + start) #Wait to check Tim's rating so we don't get rate limited
        

