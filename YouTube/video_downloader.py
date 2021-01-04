import pytube
import os

path = '/videos'

def menu():

    option = 0

    print("Choose one of the options below:")
    print("1- Download one video")
    print("2- Download a list of videos")
    print("3- Exit")

    while option not in [1, 2, 3]:
        option = int(input("Enter your option: "))

    return option

def scraper(link):

    if type(link) == str:

        #verify if the link is valid
        try:

            #get the video
            video = pytube.YouTube(link)
            print("Downloading video: " + video.title)

            if not os.path.exists(os.getcwd() + path):
                os.mkdir(os.getcwd() + path)
            
            os.chdir(os.getcwd() + path)

            #download video
            down = video.streams.get_highest_resolution()
            down.download()
            print(video.title + " downloaded!")
        except pytube.exceptions.RegexMatchError:
            print("Please enter a valid link!")
    else:
        
        if not os.path.exists(os.getcwd() + path):
            os.mkdir(os.getcwd() + path)
        
        os.chdir(os.getcwd() + path)

        for l in link:

            #verify if the link is valid
            try:

                #download video
                video = pytube.YouTube(l)
                print("Downloading video: " + video.title)

                #download the videos
                down = video.streams.get_highest_resolution()
                down.download()
                print(video.title + " downloaded!")   

            except pytube.exceptions.RegexMatchError:
                print("Please enter a valid link!") 

if __name__ == "__main__":
    
    option = menu()

    if option == 1:
        youtube_video_link = input('Enter the YouTube video link: ')
        scraper(youtube_video_link)

    elif option == 2:
        
        link = ''
        videos_list = []

        while link != '0':
            link = input('Enter the ' +str(len(videos_list)+1)+ ' YouTube video link (Enter 0 to stop): ')

            if link != '0':
                videos_list.append(link)
        
        scraper(videos_list)
    else:
        exit(1)