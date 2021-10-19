from bs4 import BeautifulSoup
import requests
import re,json

# 1407

# TODO : for patents example profile sample : 415   #comepleted 
# TODO : for no qualification section sample : 1473 #comepleted
# TODO : for multiple education sample : 4413,1     #comepleted
# TODO : for projects : 1 , 152985                  #comepleted


#TODO : Temporary
# url = 'https://vidwan.inflibnet.ac.in/profile/152985'

# Creating HTML soup to extract the data
def author_profile(url):
    r = requests.get(url)
    content = r.content
    soup = BeautifulSoup(content, 'html5lib')

    # Defined a func. to extract author name from the soup
    def author_name():
        name_tag = soup.find_all("h1")
        h1_tag = name_tag[0]
        span_tag = h1_tag.contents[0]
        author_name.name = span_tag.contents[0]
        # print(f"Name : {author_name.name}")


    # Defined a func. to extract author's affiliation from the soup
    def author_affiliation():
        aff_ini = soup.find_all('div', class_='name-location' )
        span_tag = aff_ini[0].find_all('span')
        author_affiliation.aff = span_tag[1].contents[0] + ", " + span_tag[2].contents[0]
        # print(f'Affiliation : {author_affiliation.aff}')


    # Defined a func.  to extract author's research interests
    def research_interests():
        ri_ini = soup.find_all('h5',{"id": "e_s_expertise"})
        research_interests.interests = ri_ini[0].contents[1]
        # print(f"Researcher's interests : {research_interests.interests}")


    # Defined a func.  to extract author's research interests
    def author_education():
        author_education.auth_edu = []
        if len(soup.find_all('div',{"id":'list_panel_qualification'})) == 0:
            # print("No qualifications found")
            author_education.auth_edu.append("NA")
        else:

            edu_ini = soup.find_all('div',{"id":'list_panel_qualification'})
            repeat_count = len(edu_ini[0].find_all('li'))
            # To check whether edu span is available or not.
            # print("Education/Degrees :") 
            
            for education in range(repeat_count):
                if edu_ini[0].find_all('span')[education].contents[0].lstrip() == '0' :
                    author_education.qualification_span = "NA"

                # from example of prifile 40306 when span is not mentioned 61 char empy string was there.
                elif len(edu_ini[0].find_all('span')[education].contents[0]) == 61 :
                    author_education.qualification_span = "NA"
                else:
                    author_education.qualification_span = edu_ini[0].find_all('span')[education].contents[0].lstrip()
                author_education.qualification = edu_ini[0].find_all('h2')[education].contents[0].rstrip()
                
                # TO check whether name of college/university is available from which they got their degree.
                if len(edu_ini[0].find_all('p')[education]) == 0 :
                    author_education.qualified_from = 'NA'
                else:
                    author_education.qualified_from = edu_ini[0].find_all('p')[education].contents[0]
                    
                
                # print(f"{education + 1}.  {author_education.qualification}({author_education.qualified_from}), Pass out : {author_education.qualification_span}  ")
                # author_education.education_info = str(f"{education + 1}.  {author_education.qualification}({author_education.qualified_from}), Pass out : {author_education.qualification_span}  ")
                author_education.auth_edu.append(f"{education + 1}.  {author_education.qualification}({author_education.qualified_from}), Pass out : {author_education.qualification_span}  ")

    # Authors prior affiliations
    def prior_affiliations():
        prior_affiliations.pa_list=[]
        if len(soup.find_all('div',{"id":'list_panel_experience'})) == 0:
            # print("No qualifications found")
            prior_affiliations.pa_list.append("NA")
        else:
            
            pa_ini = soup.find_all('div',{"id":'list_panel_experience'})
            pa_content = pa_ini[0].find_all("li")
            # print("Prior affiliations : ")
            for i in range (len(pa_content)):
                prior_affiliations.pa = pa_content[i].find_all("h2")[0].contents[0].rstrip().replace("\n","")
                prior_affiliations.pa_span = pa_content[i].find_all('span')[0].contents[0].replace(" ","").replace("\n","")
                prior_affiliations.aff_from = pa_content[i].find_all("p")
                for j in range (len(prior_affiliations.aff_from)):
                    prior_affiliations.aff_fin =prior_affiliations.aff_from[0].contents[0] + "" + prior_affiliations.aff_from[1].contents[0]
                prior_affiliations.pa_list.append(f"{i+1}. {prior_affiliations.pa}, {prior_affiliations.aff_fin}({prior_affiliations.pa_span})")
                # print(f"{i+1}. {prior_affiliations.pa}, {prior_affiliations.aff_fin}({prior_affiliations.pa_span})")
            # print(pa_list)

    # Authors registered patents (if any)
    def author_patents():
        author_patents.patents_list = []
        if len(soup.find_all('div',{'id' : "list-pt"})) == 0 :
            # print("Patents : NA")
            author_patents.patents_list.append('NA')
        else:
            patents_ini = soup.find_all('div',{'id' : "list-pt"})
            pt = patents_ini[0].find_all('h2')
            # print(f"Patents :")
            
            for patent in range(len(pt)):
                x = pt[patent].contents[0].lstrip()
                author_patents.patents_list.append(f"{patent + 1 } : {x}") 
                # print(f"{patent + 1 } : {x}")


    # Authors Projects (if any)
    def author_projects():
        author_projects.projects_list = []
        if len(soup.find_all('div',{'id' : "list-rp"})) == 0 :
            author_projects.projects_list.append("NA")
        else:
            patents_ini = soup.find_all('div',{'id' : "list-rp"})
            pt = patents_ini[0].find_all('h2')
            # print(f"Projects :")
            for patent in range(len(pt)):
                x = pt[patent].contents[0].lstrip()
                author_projects.projects_list.append(f"{patent + 1 } : {x}")
                # print(f"{patent + 1 } : {x}")


    # Authors recent 5 publications 
    def author_publications():
        author_publications.nameofpub=[]
        author_publications.linkofpub=[]
        # print(soup.find_all('span', {'id':'i_google_sid'}))
        # Will display google scholar publications if available 
        if len(soup.find_all('span', {'id':'i_google_sid'})) > 0:
            scholarId_ini = soup.find_all('span', {'id':'i_google_sid'})
            scholar_Id_filtering = scholarId_ini[0].find_all("a")[0].get('href')
            scholarId = scholar_Id_filtering + "&sortby=pubdate"
            # print(scholar_Id_filtering)
            #TODO scholar id filtering scraping and if not found then vidwan publications
            url="https://scholar.google.co.in/citations?hl=en&user={author_scholarId}&view_op=list_works&sortby=pubdate"
            resp=requests.get(scholarId)
            soup2=BeautifulSoup(resp.content,"html5lib")
            pub=(soup2.find("tbody",{"id":"gsc_a_b"})).find_all("a")
            
            for i in range(0,10,2):
                author_publications.nameofpub.append((pub[i].contents)[0])
                author_publications.linkofpub.append("https://scholar.google.co.in/"+(pub[i].get("href")))
            # print('Publications')
            # for i in range(5):
            #     print('--------------------------------------------')
            #     print(author_publications.nameofpub[i])
            #     print(author_publications.linkofpub[i])
            #     print('------------------------------------------')

        else:
            author_publications.nameofpub.append('NA')
            author_publications.linkofpub.append("#")




    print("*"*100)
    author_name()
    # print("--------------------------------")
    author_affiliation()
    print("--------------------------------")
    prior_affiliations()
    # print("--------------------------------")
    research_interests()
    # print("--------------------------------")
    author_education()
    # print("--------------------------------")
    author_patents()
    # print("--------------------------------")
    author_projects()
    # print("--------------------------------")
    author_publications()
    # print("*"*100)
    
    author_profile.authorprofiledata = {
        'name':author_name.name,
        "affiliation":author_affiliation.aff,
        'pa':prior_affiliations.pa_list,
        'ri':research_interests.interests,
        'authedu':author_education.auth_edu,
        'authpatents':author_patents.patents_list,
        'authprojects' : author_patents.patents_list,
        'authpub':author_publications.nameofpub,
        'authpublink': author_publications.linkofpub
        
    }
    print(author_profile.authorprofiledata)
    
    # author_profile.interests = research_interests.interests
    # author_profile.education = author_education.education_info
    # author_profile.pa = research_interests.interests
    # author_profile.patents = research_interests.interests
    # author_profile.projects = research_interests.interests
    # author_profile.publications = research_interests.interests



if __name__ == '__main__':
    # FOR TRIAL 
    author_profile('https://vidwan.inflibnet.ac.in/profile/62093')


