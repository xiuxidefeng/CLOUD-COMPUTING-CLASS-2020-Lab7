# CLOUD-COMPUTING-CLASS-2020-Lab7
# Task 7.1: Extract selected information from a newspaper webpage

![](7.1.1.png)
Check HTML structure
![](7.1.2.png)
The initial code
![](7.1.3.png)
Creating main function for debug

# Task 7.2: Obtain a subset of the movie industry to do some research  

We created a new scrapy project call scraper and spider is modified to extract the information for movies and actors participating in movies but we do not know why we always get the empty imdb file. Even though we have already tried every methods which we can search on the internet, we cannot solve it. Finally, we put the code which we think it's correct in the github.


# Task 7.3: Study the obtained data using the Elastic Stack  

Q74: Explain what you have done in the README.md file of the Lab7 folder of your answers repository, add the new plot. Push the code changes to your scrapy-lab repository (30% of total grade for this lab session)

By using Xpath library, we can get the suitable data from website, but it is difficult to crawl the text on the hyperlink.For example, <a href="/name/nm0000148/?ref_=ttfc_fc_cl_t1"> Harrison Ford</a>
we want to get the actor ID and actor name from its Xpath, but can not get the Json results although studying the Xpath basic grammar for a long time to figure out how to handle the hyperlink. 


Q75: How long have you been working on this session? What have been the main difficulties you have faced and how have you solved them?

We spent around 62 hours on learning basic skill of web scraping but encounting lots of different problems of code from the python environment to configurations. In addition, we spent lots of time on understanding code and trying different ways from the internet to solve the problems. Unfortunately, we cannot solve the problem about our code so both of us think there are no problem with our code but it keep generating an empty imdb.json. Finally, we just put the code which we think it's correct for task2 and task3.
