import nltk
import numpy as np
import re
from nltk.tag import pos_tag, map_tag
from nltk.corpus import gutenberg
import pickle
import re

#tagged = nltk.corpus.brown.tagged_words(tagset='universal')

##############DON'T NEED THIS BUSINESS###############
##emma = gutenberg.words('austen-emma.txt')
##pers = gutenberg.words('austen-persuasion.txt')
##sense = gutenberg.words('austen-sense.txt')
##blake = gutenberg.words('blake-poems.txt')
##bryant = gutenberg.words('bryant-stories.txt')
##buster = gutenberg.words('burgess-busterbrown.txt')
##alice = gutenberg.words('carroll-alice.txt')
##ball = gutenberg.words('chesterton-ball.txt')
##brown = gutenberg.words('chesterton-brown.txt')
##thurs = gutenberg.words('chesterton-thursday.txt')
##par = gutenberg.words('edgeworth-parents.txt')
##mob = gutenberg.words('melville-moby_dick.txt')
##paradise = gutenberg.words('milton-paradise.txt')
##caesar = gutenberg.words('shakespeare-caesar.txt')
##hamlet = gutenberg.words('shakespeare-hamlet.txt')
##leaves = gutenberg.words('whitman-leaves.txt')
##t = nltk.pos_tag(leaves)
##simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in t]
##with open('leaves.txt', 'wb') as f:
##    pickle.dump(simplifiedTags, f)
    
with open('emma.txt', 'rb') as f:
    emma_tagged = pickle.load(f)
with open('persuasion.txt', 'rb') as f:
    persuasion_tagged = pickle.load(f)
with open('sense.txt', 'rb') as f:
    sense_tagged = pickle.load(f)
with open('blake.txt', 'rb') as f:
    blake_tagged = pickle.load(f)
with open('bryant.txt', 'rb') as f:
    bryant_tagged = pickle.load(f)
with open('buster.txt', 'rb') as f:
    buster_tagged = pickle.load(f)
with open('alice.txt', 'rb') as f:
    alice_tagged = pickle.load(f)
with open('ball.txt', 'rb') as f:
    ball_tagged = pickle.load(f)
with open('brown.txt', 'rb') as f:
    brown_tagged = pickle.load(f)
with open('thurs.txt', 'rb') as f:
    thurs_tagged = pickle.load(f)
with open('par.txt', 'rb') as f:
    par_tagged = pickle.load(f)
with open('mob.txt', 'rb') as f:
    mob_tagged = pickle.load(f)
with open('paradise.txt', 'rb') as f:
    paradise_tagged = pickle.load(f)
with open('caesar.txt', 'rb') as f:
    caesar_tagged = pickle.load(f)
with open('hamlet.txt', 'rb') as f:
    hamlet_tagged = pickle.load(f)
with open('leaves.txt', 'rb') as f:
    leaves_tagged = pickle.load(f)


#########
#this is prediction part

def tag_input(sentence):
    mystr = sentence
    tok = re.sub("[^\w]", " ", mystr).split()
    nltk.download('punkt')
    tagged_input = nltk.pos_tag(tok)
    simplified_tags = [(word, map_tag('en-ptb','universal', tag)) for word, tag in tagged_input]
    return simplified_tags

def similar_sentence(sentence, universal_tagged_corpus):
    length = len(sentence)
    final_similar = []
    i=0
    start=0
    end=length
    while i<len(universal_tagged_corpus)-length:
        compare = universal_tagged_corpus[start:end]
        j=0
        first_similar = []
        while j<len(compare):
            if sentence[j][1] == compare[j][1]:
                first_similar+=[compare[j][0]]
                j+=1
            else:
                break;
        if len(first_similar)==length:
            final_similar+=[first_similar]
        start+=length
        end+=length
        i+=1
    return final_similar

def similar(sentence, corpus):
    length = len(sentence)
    final_similar = []
    i=0
    start=0
    end=length+1
    while i<len(corpus)-(length+1):
        compare = corpus[start:end]
        j=0
        first_similar = []
        while j<len(compare)-1:
            if sentence[j][1] == compare[j][1]:
                first_similar+=[compare[j][0]]
                j+=1
            else:
                break;
        if len(first_similar)==length:
            first_similar+=[compare[j][0]]
            final_similar+=[first_similar]
        if j!=0:
            start+=j
            end+=j
            i+=j
        else:
            start+=1
            end+=1
            i+=1
    return final_similar

def both_sides(first_half, empty_index, second_half, universal_tagged_corpus):
    full = first_half + [('','')] + second_half
    length = len(full)
    final_similar = []
    i=0
    start=0
    end=length
    while i<len(universal_tagged_corpus)-length:
        compare = universal_tagged_corpus[start:end]
        first_similar=[]
        j=0
        while j<len(first_half):
            if full[j][1] == compare[j][1]:
                first_similar+=[compare[j][0]]
                j+=1
            else:
                break
        if len(first_similar)==len(first_half):
            first_similar+=[compare[j][0]]
        if len(first_similar)==len(first_half)+1:
            k=len(first_half)+1
            while k<len(full):
                if full[k][1] == compare[k][1]:
                    first_similar+=[compare[k][0]]
                    k+=1
                else:
                    break
        if len(first_similar)==length:
            final_similar+=[first_similar]
        start+=length
        end+=length
        i+=length
    final = count_frequencies(final_similar, empty_index)
    return final


def count_frequencies(similar_list, index):
    freqs = []
    freqs+=[[similar_list[0][index],1]]
    i=1
    while i<len(similar_list):
        count = 0
        for line in freqs:
            if line[0]==similar_list[i][index]:
                line[1]+=1
                break;
            else:
                count+=1
        if count==len(freqs):
            freqs+=[[similar_list[i][index],1]]
        i+=1
    return freqs

    

def print_freqs(freq_list):
    for word in freq_list:
        print(word)

##parts of speech are:
##      ADV, NOUN, VERB, ADJ
def get_missing(first_half, pos, second_half):
    full = first_half + [('',pos)] + second_half
    return full
    
def find(sentence, empty_index, universal_tagged_corpus):
    length = len(sentence)
    final_similar = []
    i=0
    start=0
    end=length
    while i<len(universal_tagged_corpus)-length:
        compare = universal_tagged_corpus[start:end]
        j=0
        first_similar = []
        while j<len(compare):
            if sentence[j][1] == compare[j][1]:
                first_similar+=[compare[j][0]]
                j+=1
            else:
                break
        if len(first_similar)==length:
            final_similar+=[first_similar]
        if j!=0:
            start+=j
            end+=j
            i+=j
        else:
            start+=1
            end+=1
            i+=1
    final = count_frequencies(final_similar, empty_index)
    return final
    
# e needs to be the number of words before the blank #
#the pos tagger doesn't work as well when the sentence is not complete
#soooo, I need to somehow complete the sentences
#maybe instead of a blank, have a verb, noun, adjective, or adverb
#changed
##tok = "he fundamentally the terms"
##t = tag_input(tok)
##e = 2
##first = t[:e]
##second = t[e:]
##fr = both_sides(first, e, second, tagged)
##fr2 = both_sides(first, e, second, emma_tagged)
##fr3 = both_sides(first, e, second, blake_tagged)
##fr4 = both_sides(first, e, second, alice_tagged)
##fr5 = both_sides(first, e, second, ball_tagged)
##fr6 = both_sides(first, e, second, brown_tagged)
##fr7 = both_sides(first, e, second, thurs_tagged)
##fr8 = both_sides(first, e, second, par_tagged)
##fr9 = both_sides(first, e, second, mob_tagged)
##fr10 = both_sides(first, e, second, paradise_tagged)
##fr11 = both_sides(first, e, second, caesar_tagged)
##fr12 = both_sides(first, e, second, hamlet_tagged)
##fr13 = both_sides(first, e, second, leaves_tagged)

data = [emma_tagged, blake_tagged, alice_tagged, ball_tagged, brown_tagged, thurs_tagged, par_tagged, mob_tagged, paradise_tagged, leaves_tagged]

def join_data(similar_list):
    new_lines = []
    for line in similar_list:
        new_line = " ".join(line)
        new_lines+=[new_line]
    return new_lines

def collect_data(tagged_input, corpus_list):
    final_corpus = []
    for corpus in corpus_list:
        sim = similar(tagged_input, corpus)
        #sim_joined = join_data(sim)
        #final_corpus+=sim_joined
        final_corpus+=sim
    return final_corpus

def join_collected(collected_data):
    joined = []
    for line in collected_data:
        new_line = " ".join(line)
        joined+=[new_line]
    return joined
    
def pre_organize(freq_list):
    max_num = 0
    max_tup = freq_list[0]
    for tup in freq_list:
        if tup[1]>=max_num:
            max_num=tup[1]
            max_tup=tup
    return max_tup;

def organize_freqs(freq_list):
    organized = []
    while len(freq_list)>0:
        max_tup = pre_organize(freq_list)
        organized+=[max_tup]
        freq_list.remove(max_tup)
    return organized

def alpha_freqs(freq_list):
    az = []
    for word in freq_list:
        az+=[word[0]]
    az = sorted(az)
    final = []
    for word in az:
        if re.search('[a-z]', word[0]):
            final+=[word]
    return final
            


        
