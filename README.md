# **Tutorial Progress Tracker**

**A lightweight dashboard for tracking learning progress and goals. The only requirement being the progress and target should be quantified over a period of time. The app visualizes both planned and actual progress over time, supports multiple projects, and provides an interface for data updates.**

#### Built using: **[Streamlit](https://streamlit.io/)**

## **🚀 Features**

* Track multiple courses with:

    * Planned completion trajectory

    * Actual cumulative progress

    * Automated performance visualization

* Course visibility filtering (show/hide specific tracks)

* Configurable per-course parameters:

    * Start date

    * Target days

    * Target videos/pages/units etc.

* Admin update panel for logging progress per day

* Persistent storage via progress.csv

* Cloud deployable via Streamlit Community Cloud

## **🛠️ TO-DO**
- [ ] Data storage and retention through SqLite
- [ ] Enabling notifications through SMTP (Simple Mail Transfer Protocol)
- [ ] Multi-user accounts
- [ ] Better authentication way

## **📸 UI Preview**

### **User panel**
![](images/user_dashboard_preview.png)

### **Admin panel**
![](images/admin_panel_preview.png)

## **📦 Project Structure**

    project_tracker/
    ├── images/
    │── LICENSE   
    ├── README.md
    ├── requirements.txt
    └── src
        ├── data
        │   ├── course_config.json
        │   └── progress.csv
        ├── tracker.py
        └── utils
            ├── db_ops.py


## **🛠 Installation**
1. Clone the repository:

```bash
git clone https://github.com/Sunpreet29/project-tracker.git
cd project-tracker
```

2. Install dependencies after creating/choosing your virtual environment:
```bash
pip install -r requirements.txt

```

3. Open VSCode and enable the option to run inside the container
```bash
code .
```
4. Run locally (password for admin panel inside tracker.py file):
```bash
streamlit run src/tracker.py
```

## **📊 How It Works**
Each learning/tracking objective defines:

- start_date : date on which you want to start tracking your progress
- target_days : days alloted for completion
- target_units : total units of the tracked goal (videos, pages of a book, chapters etc.)
- units-completed : actual daily progress

The dashboard generates:
* **Planned trajectory** (linear)
* **Target progress till the given day**
* **Actual cumulative curve**
* **Difference over time**

## **☁️ Deployment**

This app can be deployed for free using Streamlit Community Cloud:

1. Push repository to GitHub

2. Go to https://streamlit.io/cloud

3. Deploy and link to src/tracker.py

4. Set progress.csv to be tracked and committed for persistence

### **The best part?**
### **Anyone with link of your Streamlit app can see your progress from anywhere with just a device with internet, the way to make oneself accountable too at the same time!!**