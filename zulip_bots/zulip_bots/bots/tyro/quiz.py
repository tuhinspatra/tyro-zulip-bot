import requests,random

def quiz_content(bot_handler,msg_content):
    topic = ["GK","MUSIC","FILM","SPORTS","SCIENCE","POLITICS","COMICS","ANIME","CARTOON","MATHS","COMPUTER","VEHICLES"]
    code = [9,12,11,21,17,24,29,31,32,19,18,28]
    cat = msg_content[1].upper()
    print(cat)
    if cat in topic:
        cat = code[topic.index(cat)]
        quiz_req = requests.get('https://opentdb.com/api.php?type=multiple&amount='+msg_content[0]+'&category='+str(cat)+'&difficulty='+msg_content[2]).json()
        global no_of_question,dummy,score,corr_ans_list 
        no_of_question = len(quiz_req['results'])
        score =0
        dummy = no_of_question
        question_list = ''
        corr_ans_list = ''
        j=1
        for question in quiz_req['results']:
            question_list += '\n'+str(j)+'. '+question['question']+'\n\n'
            for i in random.sample(range(4),4):
                if i == 0:
                    bot_handler.storage.put(str(j),str(i+1))
                    question_list += str(i+1)+'. '+question['correct_answer']+'\n'
                    corr_ans_list += str(j) + '. '+question['correct_answer']+'\n'
                else:
                    question_list += str(i+1)+'. '+question['incorrect_answers'][i-1]+'\n'
            j = j+1
        return question_list
    else:
        q_ref = msg_content[0]
        if int(q_ref)>no_of_question:
            msg = "**invalid question number**\n" 
        elif bot_handler.storage.get(q_ref) == str(100):
            msg = "already attempted ** try next ** :octopus:"
        else:
            dummy = dummy - 1
            ans_ref = msg_content[1]
            correct_answer = bot_handler.storage.get(q_ref)
            bot_handler.storage.put(q_ref,str(100))
            if correct_answer == ans_ref:
                msg = "**correct answer**\n"
                score = score +1
            else:
                msg = "**incorrect answer**\n"
            if dummy == 0:
                bot_handler.storage.put("a","0")
                msg += "\nyour score is "+str(score)+"/"+str(no_of_question)+"\n**correct answers :**\n"+corr_ans_list+"\nquiz over.\n**try another.**" 
        

        return msg