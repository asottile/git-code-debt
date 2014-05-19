[![Build Status](https://travis-ci.org/asottile/git-code-debt.svg?branch=master)](https://travis-ci.org/asottile/git-code-debt)

git-code-debt
=============

A dashboard for monitoring code debt in a git repository.


How-To
======




    (09:35:03 PM) asottile@yelp.com: it's fairly easy to generate yourself you know
    (09:35:11 PM) asottile@yelp.com: git clone git@github.com:asottile/git-code-debt
    (09:35:15 PM) asottile@yelp.com: cd git-code-debt
    (09:35:16 PM) asottile@yelp.com: make
    (09:35:17 PM) buck@yelp.com/F375F58F: how could i know
    (09:35:18 PM) buck@yelp.com/F375F58F: impossible
    (09:35:20 PM) asottile@yelp.com: source py_env/bin/activate
    (09:35:36 PM) asottile@yelp.com: python -m git_code_debt.create_tables yelp_cheetah.db
    (09:35:52 PM) asottile@yelp.com: python -m git_code_debt.generate git@github.com:bukzor/yelp_cheetah yelp_cheetah.db
    (09:36:00 PM) asottile@yelp.com: python -m git_code_debt_server.app yelp_cheetah.d
