**🏟️ Balanced Team Creator**
A smart Python utility to generate fair and balanced teams for sports like football, basketball, or gaming. The script ensures that matches are competitive by distributing players based on their skill levels while maintaining a level of randomness for variety.

🚀 Overview
Setting up a match can be difficult when skill levels vary. This tool automates the process by:

Reading player data from a text file.

Filtering out players who are unavailable.

Balancing teams using a "Pot-based Shuffle" (pairing top players and splitting them randomly).

📊 How the Balancing Works
The script doesn't just randomly pick names. It follows a logic to ensure fairness:

Pot System: Players are sorted by points and grouped into pairs (e.g., the two best players, then the next two).

Random Split: From each pair, one player is randomly sent to Team A and the other to Team B.

Result: Teams have nearly identical total skill points, but the lineups change every time you run the script.

📁 File Format
Your teams.txt (or any .txt file) should follow this 3-column structure: Name Points Status (O: Playing, X: Not Playing)

Fatih 90 O
Kutay 70 O
Gökhan 30 O
Yusuf 70 O
Onur 80 X

🛠️ Usage
Clone the repository or copy the script.

Ensure you have a .txt file with at least 14 players marked with O.

Run the script:

`python main.py
`
💻 Code Structure
createRandomTeam(file_name): The core engine that handles file I/O, filtering, and the balancing algorithm.

printerFunction(name, team): Formats and displays the results with total team strength.

--- A TEAM (Total Point: 520.0) ---
- Fatih (90.0)
- Yusuf (70.0)
- Hasan (80.0)
...

--- B TEAM (Total Point: 515.0) ---
- Soner (90.0)
- Semih (70.0)
- Burak (90.0)
...