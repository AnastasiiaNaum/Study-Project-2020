# Study-Project-2020
Development of a system for predicting the successful completion of a subject

Results of classterisation are in file Progect_results

API Requests description:

http://127.0.0.1:5000/all_exps : 

   GET  (returns existing experiments and results)

   POST (creates new empty experiment)

http://127.0.0.1:5000/all_exps/{exp_id} : 

   GET   (returns results to the experiment given)

   POST  (begins experiment with given id, requires parameters)
