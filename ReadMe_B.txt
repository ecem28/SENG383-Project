KidTask Coding Implementation — Student B

This folder contains the KidTask system implementation created using Cursor AI.
All logic is implemented inside main.py, including:

- User class with roles (parent, child)
- Task assignment and completion logic
- Permission checks and error handling
- Simple modular design

All code written and reviewed by Student B.


UPDATE - BeePlan Project
Final Presentation Video (Student B) 
https://drive.google.com/file/d/1bS1tHpMluRcybvjywD2KOFsYbMpA_BWc/view?usp=sharing

The BeePlan system has been implemented as part of the project.

My recent contributions as Student B:

- Algorithm: Even distribution of classes over 5 days

- Restriction: Maximum 4 hours of instructor classes per day

- Reporting: Turkish language verification reports page.

AI Analysis Card:

Prompt: "Add a maximum of 4 hours of instructor classes per day."
AI Output: Completely removed the 5-hour class.

---

 BeePlan - Lesson Planning System (Student B Update)

 Technical Implementation and Algorithm — Student B (Gizem Kılıç)

- **Advanced Scheduling Algorithm:**  logic was applied to distribute lessons evenly across the weekly schedule.
- **Constraint Management:** A **maximum 4-hour** daily lesson limit for instructors was integrated into the system.
- **SENG383 Special Solution:** Lessons exceeding 4 hours (5 hours) are automatically **split (Split Logic)** without disrupting the instructor's workload.
- **Dynamic Integration:** Instant transfer of data generated on the Generate Schedule page to the **Timetable** and **Reports** pages was implemented.
- **Verification System:** A fully Turkish **Verification Reports** screen was developed to check all rule violations.


---

 AI Usage Analysis (Student B)


| **Scheduling Algorithm** | Github Copilot | "Write a conflict-free Python function that spreads classes over days." | Only filled the first 2 days. | Manually added Round Robin loop. |
| **Instructor Load Control** | Gemini | "Add a maximum instructor limit of 4 hours per day." | Removed 5-hour lessons like SENG383. | Lesson splitting logic added manually. |
| **Reporting System** | Cursor | "Translate the Validation reports page into Turkish and pull data into the table." | Headings remained in English. | The entire interface was translated into Turkish and data flow was connected. |

---

 Installation and Running

The project runs with **Python 3.10+** version. The necessary libraries are standard Python libraries.

```bash
# To run the project:
python main.py

#default user
admin

demo
login 
add course 
delete selected
generate schedule
timetable
back to course selection
reports
log out
