# 2048.py

# importing the logic.py file
# where we have written all the
# logic functions used.
import logic
import ai_testing
import multiprocessing as mp

# Driver code
output = mp.Queue()
def test_one(output):
	params = ai_testing.init_params([16,8,4])
	cost_history = []

	# modifications with cost function
	num_moves = 0  
	highest_tile = 0 
	
	# calling start_game function
	# to initialize the matrix
	mat = logic.start_game()
	status = logic.get_current_state(mat)
	while(status != 'LOST'):
		sols, trash = ai_testing.forward_prop(ai_testing.flatten(mat), params)
		# taking the user input
		# for next step
		new_sols = sorted(sols)
		curr = 3
		old_mat = mat
		# we have to move up
		while (curr != -1) and (old_mat == mat) :
			if(new_sols[curr] == sols[0]):

				# call the move_up function
				mat, flag = logic.move_up(mat)

				# get the current state and print it
				status = logic.get_current_state(mat)
				print(status)

				# if game not over then continue
				# and add a new two
				if(status == 'GAME NOT OVER'):
					logic.add_new_2(mat)

				# else break the loop 

			# the above process will be followed
			# in case of each type of move
			# below

			# to move down
			elif(new_sols[curr] == sols[1]):
				mat, flag = logic.move_down(mat)
				status = logic.get_current_state(mat)
				print(status)
				if(status == 'GAME NOT OVER'):
					logic.add_new_2(mat)

			# to move left
			elif(new_sols[curr] == sols[2]):
				mat, flag = logic.move_left(mat)
				status = logic.get_current_state(mat)
				print(status)
				if(status == 'GAME NOT OVER'):
					logic.add_new_2(mat)

			# to move right
			elif(new_sols[curr] == sols[3]):
				mat, flag = logic.move_right(mat)
				status = logic.get_current_state(mat)
				print(status)
				if(status == 'GAME NOT OVER'):
					logic.add_new_2(mat)
			else:
				print("Invalid Key Pressed")
			curr = curr - 1
		
		num_moves += 1
		highest_tile = max(max(row) for row in mat)
	
		# print the matrix after each
		# move.
		logic.print_grid(mat)
	print("GAME OVER")

	# modifications
	final_score = sum(sum(row) for row in mat)
	game_cost = ai_testing.cost_function(final_score, num_moves, highest_tile)
	output.put((params, game_cost)) 
	# output.put((params, 30))

	

if __name__ == '__main__':
	processes = []
	for i in range(10):
		processes.append(mp.Process(target=test_one, args=(output,)))

	for p in processes:
		p.start()

# Exit the completed processes
	for p in processes:
		p.join()

	print('finished1')
	results = []
	for p in processes:
		print('once')
		# modified
		params, cost = output.get()
		results.append((params, cost))
		# results.append(output.get())
	
	# sorting results by cost, goal to minimize the negative of the desired maximum
	results.sort(key=lambda x: x[1])

	best_params = results[0][0]
	print("Best parameters:", best_params)
	print("Best cost:", results[0][1])

	# print(results)
	print('Finished')