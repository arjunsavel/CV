"""
Counts the number of submitted and unreviewed pubs.

author: @arjunsavel
"""

def count_pubs(filename):
    """
    from a reasonably formatted .tex file, counts the number of publications.

    Input
    ------
        :filename: (str) full path to file.

    Output
    ------
        :n_pubs: (int) number of pubs in file
        :n_first: (int) number of first-author pubs in file
    """
    
    f = open(filename)
    f1 = f.readlines()
    f.close()

    n_pubs = 0

    # iterate through file
    for line in f1:

        # all the publications are in list form, beginning with "\item" for each one!
        if '\item' in line:
            n_pubs += 1

    return n_pubs


if __name__ == "__main__":
    n_unref, n_first_unref = count_pubs('../supp_tex/pubs_unref.tex')
    n_submitted, n_first_submitted = count_pubs('../supp_tex/pubs_submitted.tex')

    n_pubs = n_unref + n_submitted
    # write to file
    with open('../supp_tex/n_review.tex', 'w') as f:
        f.wite(n_pubs)

    with open('../supp_tex/n_first_submit.tex', 'w') as f:
        f.wite(n_first_submitted)
        
