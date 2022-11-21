# capacitated-team-orienteering-problem
### A local search algorithm algorithm for the team orienteering problem.

In the team orienteering problem, start and end depots are specified along with other locations which have associated demands, service times and profits.
Given a fixed amount of time for each of the M vehicles of the team,
the goal is to determine M paths from the start point to the end point through a subset of locations in order to maximize the total profit.

## Technics used :

* **Heuristic algorithm**

  * The first step is to design a simple heuristic algorithm that calculates the ratio $\dfrac{distance + service time + demand}{profit}$.
  The algorithm greedily selects customers form an Restricted Candidate List until all vehicles are full.

* **Local search**

  * The next step is to find ways to improve the solution created from the heuristic without examining all possible senarios. This is done by implementing local search operators that afect the solution in a way that differs by a little from the previous one.
  
    Operators :
   
      1. Relocate
        
          Relocate is the process where a selected node (target) is moved from its current position in the route to another position (destination).
          
      2. Two opt
      
          The idea of 2-opt is to exchange the links between two pairs of subsequent nodes.

      3. Node addition
      
          The two previous operators are focued on redusing the travel time of the routes. 
          Next step is to try and improve the solution by adding new nodes and subsequently gain more profit.

      4. Destroy and repair
      
          This operator focuses on destroying a part of the solution and then reconstructing with an other node to differentiate the solution.

