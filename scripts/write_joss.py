import numpy as np

# read in lines from tex file
f = open('../main.tex', 'r')
f1 = f.readlines()
f.close()

# assume scrape_joss.py has already been run
num_reviewed = int(np.loadtxt('../data/num_joss_reviews.txt'))

if num_reviewed == 1:
    project_word = 'project'
else:
    project_word = 'projects'
    
reviewed_line = f'\\item Reviewer, Journal of Open Source Software ({num_reviewed} {project_word} reviewed) (2020)\n'
    
for i, line in enumerate(f1):
    if 'Reviewer, Journal of Open Source Software' in line:
        f1[i] = reviewed_line
        break
        
# write back to file
f = open('../main.tex', 'w')
f.writelines(f1)
f.close()
