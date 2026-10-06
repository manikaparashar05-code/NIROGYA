import streamlit as st
import requests
import joblib
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NIROGYA",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------
# SESSION STATE
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# -----------------------------
# LOGIN / REGISTER PAGE
# -----------------------------

if not st.session_state.logged_in:

    st.title("🧬 NIROGYA")
    st.subheader("AI-Powered Disease Risk & Health Analytics")
    st.write("")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    # -------------------------
    # LOGIN
    # -------------------------

    with login_tab:

        st.subheader("Login")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            if not email or not password:
                st.warning("Please enter email and password.")

            else:

                try:

                    response = requests.post(
                        "http://127.0.0.1:8000/login",
                        json={
                            "email": email,
                            "password": password
                        }
                    )

                    if response.status_code == 200:

                        st.session_state.logged_in = True
                        st.session_state.user = response.json()

                        st.success("Login successful!")
                        st.rerun()

                    else:

                        try:
                            detail = response.json().get(
                                "detail",
                                "Invalid email or password."
                            )
                        except:
                            detail = "Invalid email or password."

                        st.error(detail)

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Backend is not running. "
                        "Please start FastAPI first."
                    )


    # -------------------------
    # REGISTER
    # -------------------------

    with register_tab:

        st.subheader("Create Account")

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        reg_email = st.text_input(
            "Email",
            key="register_email"
        )

        reg_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not name or not reg_email or not reg_password:

                st.warning(
                    "Please fill all the fields."
                )

            else:

                try:

                    response = requests.post(
                        "http://127.0.0.1:8000/register",
                        json={
                            "full_name": name,
                            "email": reg_email,
                            "password": reg_password,
                            "role": "patient"
                        }
                    )

                    if response.status_code in [200, 201]:

                        st.success(
                            "Account created successfully! "
                            "You can now login."
                        )

                    else:

                        try:
                            detail = response.json().get(
                                "detail",
                                "Registration failed."
                            )
                        except:
                            detail = "Registration failed."

                        st.error(detail)

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Backend is not running. "
                        "Please start FastAPI first."
                    )


    st.stop()


# -----------------------------
# USER INFORMATION
# -----------------------------

user = st.session_state.user

user_name = user.get(
    "name",
    user.get("full_name", "User")
)

user_email = user.get(
    "email",
    ""
)

user_id = user.get(
    "user_id",
    user.get("id")
)


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("🧬 NIROGYA")

st.sidebar.write(
    f"Welcome, **{user_name}**"
)

if user_email:
    st.sidebar.caption(user_email)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🩺 Disease Prediction",
        "📊 Health Analytics",
        "👥 Patient Clustering",
        "🔎 Anomaly Detection",
        "🔗 Association Rules",
        "🧠 Explainable AI",
        "⛏️ Data Mining",
        "📜 History"
    ]
)

st.sidebar.divider()

if st.sidebar.button(
    "Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user = None

    st.rerun()


# -----------------------------
# DATASET LOADER
# -----------------------------

@st.cache_data
def load_dataset():

    return pd.read_csv(
        "data/diabetes.csv"
    )


# -----------------------------
# DASHBOARD
# -----------------------------

if page == "🏠 Dashboard":

    st.title("🏠 NIROGYA Dashboard")

    st.write(
        "AI-powered disease risk and healthcare analytics platform."
    )

    try:

        df = load_dataset()

        total_patients = len(df)

        diabetes_cases = int(
            (df["Outcome"] == 1).sum()
        )

        non_diabetes = int(
            (df["Outcome"] == 0).sum()
        )

        total_features = len(
            df.columns
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Patients",
                total_patients
            )

        with col2:
            st.metric(
                "Diabetes Cases",
                diabetes_cases
            )

        with col3:
            st.metric(
                "Non-Diabetes",
                non_diabetes
            )

        with col4:
            st.metric(
                "Features",
                total_features
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "Disease Distribution"
            )

            outcome_counts = (
                df["Outcome"]
                .value_counts()
                .rename({
                    0: "No Diabetes",
                    1: "Diabetes"
                })
                .reset_index()
            )

            outcome_counts.columns = [
                "Status",
                "Patients"
            ]

            fig = px.bar(
                outcome_counts,
                x="Status",
                y="Patients",
                title="Diabetes Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader(
                "Dataset Overview"
            )

            st.write(
                "NIROGYA uses a real diabetes dataset "
                "for disease prediction and data mining."
            )

            st.write(
                f"**Rows:** {df.shape[0]}"
            )

            st.write(
                f"**Columns:** {df.shape[1]}"
            )

            st.write(
                "**Machine Learning:** Logistic Regression"
            )

            st.write(
                "**Clustering:** K-Means"
            )

            st.write(
                "**Anomaly Detection:** Isolation Forest"
            )

            st.write(
                "**Explainability:** SHAP"
            )

        st.divider()

        st.subheader(
            "Prediction History Summary"
        )

        if user_id:

            try:

                history_response = requests.get(
                    f"http://127.0.0.1:8000/prediction-history/{user_id}"
                )

                if history_response.status_code == 200:

                    history = history_response.json()

                    if history:

                        history_df = pd.DataFrame(
                            history
                        )

                        if "prediction" in history_df.columns:

                            higher_risk = (
                                history_df["prediction"]
                                == "Higher Diabetes Risk"
                            ).sum()

                            lower_risk = (
                                history_df["prediction"]
                                == "Lower Diabetes Risk"
                            ).sum()

                            c1, c2, c3 = st.columns(3)

                            with c1:
                                st.metric(
                                    "Total Predictions",
                                    len(history_df)
                                )

                            with c2:
                                st.metric(
                                    "Higher Risk",
                                    int(higher_risk)
                                )

                            with c3:
                                st.metric(
                                    "Lower Risk",
                                    int(lower_risk)
                                )

                    else:

                        st.info(
                            "No prediction history available yet."
                        )

            except requests.exceptions.ConnectionError:

                st.warning(
                    "Unable to connect to backend."
                )

    except Exception as e:

        st.error(
            f"Unable to load dashboard: {e}"
        )
        # -----------------------------
# DISEASE PREDICTION
# -----------------------------

elif page == "🩺 Disease Prediction":

    st.title("🩺 Disease Risk Prediction")

    st.write(
        "Enter patient health information to estimate diabetes risk."
    )

    try:

        model = joblib.load(
            "models/diabetes_model.pkl"
        )

        st.subheader("Patient Information")

        col1, col2 = st.columns(2)

        with col1:

            pregnancies = st.number_input(
                "Pregnancies",
                min_value=0,
                max_value=20,
                value=1,
                key="pred_pregnancies"
            )

            glucose = st.number_input(
                "Glucose",
                min_value=0,
                max_value=300,
                value=120,
                key="pred_glucose"
            )

            blood_pressure = st.number_input(
                "Blood Pressure",
                min_value=0,
                max_value=200,
                value=70,
                key="pred_bp"
            )

            skin_thickness = st.number_input(
                "Skin Thickness",
                min_value=0,
                max_value=100,
                value=20,
                key="pred_skin"
            )

        with col2:

            insulin = st.number_input(
                "Insulin",
                min_value=0,
                max_value=900,
                value=80,
                key="pred_insulin"
            )

            bmi = st.number_input(
                "BMI",
                min_value=0.0,
                max_value=70.0,
                value=25.0,
                step=0.1,
                key="pred_bmi"
            )

            pedigree = st.number_input(
                "Diabetes Pedigree Function",
                min_value=0.0,
                max_value=3.0,
                value=0.5,
                step=0.01,
                key="pred_pedigree"
            )

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=30,
                key="pred_age"
            )

        st.divider()

        if st.button(
            "🔍 Predict Disease Risk",
            use_container_width=True
        ):

            patient_data = pd.DataFrame(
                [[
                    pregnancies,
                    glucose,
                    blood_pressure,
                    skin_thickness,
                    insulin,
                    bmi,
                    pedigree,
                    age
                ]],
                columns=[
                    "Pregnancies",
                    "Glucose",
                    "BloodPressure",
                    "SkinThickness",
                    "Insulin",
                    "BMI",
                    "DiabetesPedigreeFunction",
                    "Age"
                ]
            )

            prediction = model.predict(
                patient_data
            )[0]

            probability = model.predict_proba(
                patient_data
            )[0][1]

            if prediction == 1:

                result = "Higher Diabetes Risk"

                st.error(
                    f"⚠️ {result}"
                )

            else:

                result = "Lower Diabetes Risk"

                st.success(
                    f"✅ {result}"
                )

            st.metric(
                "Risk Probability",
                f"{probability * 100:.2f}%"
            )

            st.progress(
                float(probability)
            )

            st.info(
                "This prediction is based on the machine learning model "
                "and should not be considered a medical diagnosis."
            )

            # Save prediction to database

            if user_id:

                try:

                    history_response = requests.post(
                        "http://127.0.0.1:8000/prediction-history",
                        json={
                            "user_id": user_id,
                            "glucose": float(glucose),
                            "blood_pressure": float(
                                blood_pressure
                            ),
                            "bmi": float(bmi),
                            "age": int(age),
                            "pregnancies": int(
                                pregnancies
                            ),
                            "prediction": result,
                            "risk_probability": float(
                                probability
                            )
                        }
                    )

                    if history_response.status_code in [
                        200,
                        201
                    ]:

                        st.success(
                            "Prediction saved to history."
                        )

                    else:

                        st.warning(
                            "Prediction generated, "
                            "but could not be saved."
                        )

                except requests.exceptions.ConnectionError:

                    st.warning(
                        "Prediction generated, "
                        "but backend is unavailable."
                    )

    except FileNotFoundError:

        st.error(
            "Model file not found. "
            "Please train the model first."
        )

    except Exception as e:

        st.error(
            f"Prediction error: {e}"
        )


# -----------------------------
# HEALTH ANALYTICS
# -----------------------------

elif page == "📊 Health Analytics":

    st.title("📊 Health Analytics")

    try:

        df = load_dataset()

        st.subheader("Dataset Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Patients",
                len(df)
            )

        with col2:
            st.metric(
                "Average Glucose",
                f"{df['Glucose'].mean():.2f}"
            )

        with col3:
            st.metric(
                "Average BMI",
                f"{df['BMI'].mean():.2f}"
            )

        with col4:
            st.metric(
                "Average Age",
                f"{df['Age'].mean():.2f}"
            )

        st.divider()

        # Outcome distribution

        st.subheader(
            "Diabetes Distribution"
        )

        outcome_df = (
            df["Outcome"]
            .value_counts()
            .rename({
                0: "No Diabetes",
                1: "Diabetes"
            })
            .reset_index()
        )

        outcome_df.columns = [
            "Outcome",
            "Count"
        ]

        fig1 = px.bar(
            outcome_df,
            x="Outcome",
            y="Count",
            title="Diabetes Outcome Distribution"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # Glucose distribution

        st.subheader(
            "Glucose Distribution"
        )

        fig2 = px.histogram(
            df,
            x="Glucose",
            color="Outcome",
            nbins=30,
            title="Glucose Distribution by Outcome"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # BMI boxplot

        st.subheader(
            "BMI Analysis"
        )

        fig3 = px.box(
            df,
            x="Outcome",
            y="BMI",
            color="Outcome",
            title="BMI Distribution by Diabetes Outcome"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # Age vs glucose

        st.subheader(
            "Age vs Glucose"
        )

        fig4 = px.scatter(
            df,
            x="Age",
            y="Glucose",
            color="Outcome",
            hover_data=[
                "BMI",
                "BloodPressure"
            ],
            title="Age vs Glucose"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

        # Correlation

        st.subheader(
            "Feature Correlation"
        )

        correlation = df.corr(
            numeric_only=True
        )

        fig5 = px.imshow(
            correlation,
            text_auto=True,
            title="Correlation Heatmap"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

        st.subheader(
            "Dataset Description"
        )

        st.dataframe(
            df.describe(),
            use_container_width=True
        )

        st.subheader(
            "Sample Data"
        )

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Analytics error: {e}"
        )
        # -----------------------------
# PATIENT CLUSTERING
# -----------------------------

elif page == "👥 Patient Clustering":

    st.title("👥 Patient Clustering")

    st.write(
        "K-Means clustering is used to group patients "
        "with similar health characteristics."
    )

    try:

        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA

        df = load_dataset()

        clustering_features = [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "BMI",
            "Age"
        ]

        cluster_data = df[
            clustering_features
        ].copy()

        # Replace invalid zero values

        for column in [
            "Glucose",
            "BloodPressure",
            "BMI"
        ]:

            cluster_data[column] = (
                cluster_data[column]
                .replace(0, pd.NA)
            )

            cluster_data[column] = (
                cluster_data[column]
                .fillna(
                    cluster_data[column].median()
                )
            )

        scaler = StandardScaler()

        scaled_data = scaler.fit_transform(
            cluster_data
        )

        kmeans = KMeans(
            n_clusters=3,
            random_state=42,
            n_init=10
        )

        clusters = kmeans.fit_predict(
            scaled_data
        )

        cluster_df = cluster_data.copy()

        cluster_df["Cluster"] = (
            clusters.astype(str)
        )

        # PCA

        pca = PCA(
            n_components=2,
            random_state=42
        )

        pca_data = pca.fit_transform(
            scaled_data
        )

        cluster_df["PCA1"] = pca_data[:, 0]
        cluster_df["PCA2"] = pca_data[:, 1]

        # Metrics

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Number of Clusters",
                3
            )

        with col2:
            st.metric(
                "Patients Analysed",
                len(cluster_df)
            )

        with col3:
            st.metric(
                "Features Used",
                len(clustering_features)
            )

        st.divider()

        # Cluster distribution

        st.subheader(
            "Cluster Distribution"
        )

        cluster_counts = (
            cluster_df["Cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        cluster_counts.columns = [
            "Cluster",
            "Patients"
        ]

        fig1 = px.bar(
            cluster_counts,
            x="Cluster",
            y="Patients",
            title="Patients in Each Cluster"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # PCA visualization

        st.subheader(
            "Cluster Visualization"
        )

        fig2 = px.scatter(
            cluster_df,
            x="PCA1",
            y="PCA2",
            color="Cluster",
            title="Patient Clusters using PCA",
            hover_data=clustering_features
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # Cluster profiles

        st.subheader(
            "Cluster Profiles"
        )

        profile = (
            cluster_df
            .groupby("Cluster")[
                clustering_features
            ]
            .mean()
            .round(2)
        )

        st.dataframe(
            profile,
            use_container_width=True
        )

        # Feature comparison

        st.subheader(
            "Feature Distribution by Cluster"
        )

        selected_feature = st.selectbox(
            "Select Feature",
            clustering_features,
            key="cluster_feature"
        )

        fig3 = px.box(
            cluster_df,
            x="Cluster",
            y=selected_feature,
            color="Cluster",
            title=f"{selected_feature} by Cluster"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # Data

        with st.expander(
            "View Clustering Data"
        ):

            st.dataframe(
                cluster_df,
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"Clustering error: {e}"
        )


# -----------------------------
# ANOMALY DETECTION
# -----------------------------

elif page == "🔎 Anomaly Detection":

    st.title("🔎 Anomaly Detection")

    st.write(
        "Isolation Forest identifies unusual or abnormal "
        "health records in the dataset."
    )

    try:

        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import IsolationForest

        df = load_dataset()

        anomaly_features = [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ]

        anomaly_data = df[
            anomaly_features
        ].copy()

        # Replace invalid zero values

        for column in [
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI"
        ]:

            anomaly_data[column] = (
                anomaly_data[column]
                .replace(0, pd.NA)
            )

            anomaly_data[column] = (
                anomaly_data[column]
                .fillna(
                    anomaly_data[column].median()
                )
            )

        scaler = StandardScaler()

        scaled_data = scaler.fit_transform(
            anomaly_data
        )

        isolation_forest = IsolationForest(
            n_estimators=200,
            contamination=0.05,
            random_state=42
        )

        anomaly_prediction = (
            isolation_forest.fit_predict(
                scaled_data
            )
        )

        anomaly_score = (
            isolation_forest
            .decision_function(
                scaled_data
            )
        )

        result_df = df.copy()

        result_df["Anomaly Score"] = (
            anomaly_score
        )

        result_df["Anomaly"] = (
            anomaly_prediction
        )

        result_df["Status"] = result_df[
            "Anomaly"
        ].map({
            1: "Normal",
            -1: "Anomaly"
        })

        total_anomalies = int(
            (result_df["Status"] == "Anomaly").sum()
        )

        total_normal = int(
            (result_df["Status"] == "Normal").sum()
        )

        # Metrics

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Records",
                len(result_df)
            )

        with col2:

            st.metric(
                "Normal Records",
                total_normal
            )

        with col3:

            st.metric(
                "Anomalies Detected",
                total_anomalies
            )

        st.divider()

        # Status distribution

        st.subheader(
            "Anomaly Distribution"
        )

        status_counts = (
            result_df["Status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        fig1 = px.bar(
            status_counts,
            x="Status",
            y="Count",
            title="Normal vs Anomalous Records"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        # Glucose vs BMI

        st.subheader(
            "Anomaly Visualization"
        )

        fig2 = px.scatter(
            result_df,
            x="Glucose",
            y="BMI",
            color="Status",
            hover_data=[
                "Age",
                "BloodPressure",
                "Outcome"
            ],
            title="Glucose vs BMI Anomaly Analysis"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # Score distribution

        st.subheader(
            "Anomaly Score Distribution"
        )

        fig3 = px.histogram(
            result_df,
            x="Anomaly Score",
            nbins=40,
            title="Distribution of Anomaly Scores"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # Feature boxplot

        st.subheader(
            "Feature Analysis"
        )

        selected_anomaly_feature = st.selectbox(
            "Select Feature",
            anomaly_features,
            key="anomaly_feature"
        )

        fig4 = px.box(
            result_df,
            x="Status",
            y=selected_anomaly_feature,
            color="Status",
            title=f"{selected_anomaly_feature} - Normal vs Anomaly"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

        # Anomalous records

        st.subheader(
            "Detected Anomalies"
        )

        anomalies_only = (
            result_df[
                result_df["Status"] == "Anomaly"
            ]
            .sort_values(
                "Anomaly Score"
            )
        )

        st.dataframe(
            anomalies_only,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Anomaly detection error: {e}"
        )
        # -----------------------------
# ASSOCIATION RULE MINING
# -----------------------------

elif page == "🔗 Association Rules":

    st.title("🔗 Association Rule Mining")

    st.write(
        "Discover relationships and frequent patterns "
        "between patient health conditions."
    )

    try:

        from mlxtend.frequent_patterns import apriori
        from mlxtend.frequent_patterns import association_rules

        df = load_dataset()

        st.subheader("Mining Parameters")

        min_support = st.slider(
            "Minimum Support",
            min_value=0.05,
            max_value=0.50,
            value=0.10,
            step=0.05,
            key="association_support"
        )

        # Create transaction-style dataset

        association_df = pd.DataFrame()

        association_df["Glucose_High"] = (
            df["Glucose"] >= 126
        )

        association_df["BMI_High"] = (
            df["BMI"] >= 25
        )

        association_df["Age_Above_30"] = (
            df["Age"] >= 30
        )

        association_df["Pregnancies_Above_2"] = (
            df["Pregnancies"] >= 2
        )

        association_df["BloodPressure_High"] = (
            df["BloodPressure"] >= 80
        )

        association_df["Diabetes"] = (
            df["Outcome"] == 1
        )

        # Frequent itemsets

        frequent_itemsets = apriori(
            association_df,
            min_support=min_support,
            use_colnames=True
        )

        st.subheader("Frequent Itemsets")

        if frequent_itemsets.empty:

            st.warning(
                "No frequent patterns found. "
                "Try reducing minimum support."
            )

        else:

            frequent_itemsets["Itemsets"] = (
                frequent_itemsets["itemsets"]
                .apply(
                    lambda x: ", ".join(x)
                )
            )

            display_itemsets = (
                frequent_itemsets[
                    [
                        "Itemsets",
                        "support"
                    ]
                ]
                .sort_values(
                    "support",
                    ascending=False
                )
            )

            st.dataframe(
                display_itemsets,
                use_container_width=True
            )

            # Association rules

            try:

                rules = association_rules(
                    frequent_itemsets,
                    metric="confidence",
                    min_threshold=0.50
                )

            except Exception:

                rules = pd.DataFrame()

            st.subheader(
                "Association Rules"
            )

            if rules.empty:

                st.info(
                    "No strong association rules found "
                    "with the current parameters."
                )

            else:

                rules_display = rules.copy()

                rules_display["Antecedents"] = (
                    rules_display["antecedents"]
                    .apply(
                        lambda x: ", ".join(x)
                    )
                )

                rules_display["Consequents"] = (
                    rules_display["consequents"]
                    .apply(
                        lambda x: ", ".join(x)
                    )
                )

                rules_display = rules_display[
                    [
                        "Antecedents",
                        "Consequents",
                        "support",
                        "confidence",
                        "lift"
                    ]
                ].sort_values(
                    "lift",
                    ascending=False
                )

                st.dataframe(
                    rules_display,
                    use_container_width=True
                )

                st.subheader(
                    "Support vs Confidence"
                )

                fig = px.scatter(
                    rules_display,
                    x="support",
                    y="confidence",
                    size="lift",
                    hover_data=[
                        "Antecedents",
                        "Consequents",
                        "lift"
                    ],
                    title="Association Rule Strength"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.subheader(
                    "Strongest Rules"
                )

                st.dataframe(
                    rules_display.head(10),
                    use_container_width=True
                )

    except Exception as e:

        st.error(
            f"Association rule error: {e}"
        )


# -----------------------------
# EXPLAINABLE AI
# -----------------------------

elif page == "🧠 Explainable AI":

    st.title("🧠 Explainable AI")

    st.write(
        "Understand which patient features contribute "
        "most to the diabetes risk prediction."
    )

    try:

        import shap

        model = joblib.load(
            "models/diabetes_model.pkl"
        )

        st.subheader(
            "Enter Patient Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            shap_pregnancies = st.number_input(
                "Pregnancies",
                min_value=0,
                max_value=20,
                value=1,
                key="shap_pregnancies"
            )

            shap_glucose = st.number_input(
                "Glucose",
                min_value=0,
                max_value=300,
                value=120,
                key="shap_glucose"
            )

            shap_bp = st.number_input(
                "Blood Pressure",
                min_value=0,
                max_value=200,
                value=70,
                key="shap_bp"
            )

            shap_skin = st.number_input(
                "Skin Thickness",
                min_value=0,
                max_value=100,
                value=20,
                key="shap_skin"
            )

        with col2:

            shap_insulin = st.number_input(
                "Insulin",
                min_value=0,
                max_value=900,
                value=80,
                key="shap_insulin"
            )

            shap_bmi = st.number_input(
                "BMI",
                min_value=0.0,
                max_value=70.0,
                value=25.0,
                step=0.1,
                key="shap_bmi"
            )

            shap_pedigree = st.number_input(
                "Diabetes Pedigree Function",
                min_value=0.0,
                max_value=3.0,
                value=0.5,
                step=0.01,
                key="shap_pedigree"
            )

            shap_age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=30,
                key="shap_age"
            )

        st.divider()

        if st.button(
            "🧠 Explain Prediction",
            use_container_width=True
        ):

            patient_data = pd.DataFrame(
                [[
                    shap_pregnancies,
                    shap_glucose,
                    shap_bp,
                    shap_skin,
                    shap_insulin,
                    shap_bmi,
                    shap_pedigree,
                    shap_age
                ]],
                columns=[
                    "Pregnancies",
                    "Glucose",
                    "BloodPressure",
                    "SkinThickness",
                    "Insulin",
                    "BMI",
                    "DiabetesPedigreeFunction",
                    "Age"
                ]
            )

            # Get prediction

            prediction = model.predict(
                patient_data
            )[0]

            probability = model.predict_proba(
                patient_data
            )[0][1]

            if prediction == 1:

                st.error(
                    f"Prediction: Higher Diabetes Risk "
                    f"({probability * 100:.2f}%)"
                )

            else:

                st.success(
                    f"Prediction: Lower Diabetes Risk "
                    f"({probability * 100:.2f}%)"
                )

            # Extract preprocessing and classifier

            preprocessing = model[:-1]
            classifier = model[-1]

            transformed_data = (
                preprocessing.transform(
                    patient_data
                )
            )

            # Use transformed patient data as background

            background = transformed_data

            explainer = shap.LinearExplainer(
                classifier,
                background
            )

            shap_values = explainer(
                transformed_data
            )

            values = shap_values.values

            if len(values.shape) == 2:

                feature_values = values[0]

            else:

                feature_values = values

            explanation_df = pd.DataFrame(
                {
                    "Feature": patient_data.columns,
                    "SHAP Value": feature_values
                }
            )

            explanation_df["Impact"] = (
                explanation_df["SHAP Value"]
                .apply(
                    lambda x:
                    "Increases Risk"
                    if x > 0
                    else "Decreases Risk"
                )
            )

            explanation_df = (
                explanation_df
                .sort_values(
                    "SHAP Value",
                    ascending=False
                )
            )

            st.subheader(
                "Feature Contributions"
            )

            st.dataframe(
                explanation_df,
                use_container_width=True
            )

            # Visualization

            st.subheader(
                "Feature Impact"
            )

            fig = px.bar(
                explanation_df,
                x="SHAP Value",
                y="Feature",
                orientation="h",
                color="Impact",
                title="SHAP Feature Contributions"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader(
                "Top Influential Features"
            )

            top_features = (
                explanation_df
                .copy()
                .sort_values(
                    "SHAP Value",
                    key=lambda x: x.abs(),
                    ascending=False
                )
                .head(5)
            )

            st.dataframe(
                top_features,
                use_container_width=True
            )

            st.info(
                "SHAP values explain how each feature "
                "influences the model's prediction. "
                "Positive values increase the predicted risk, "
                "while negative values decrease it."
            )

    except ImportError:

        st.error(
            "SHAP is not installed. "
            "Run: pip install shap"
        )

    except Exception as e:

        st.error(
            f"Explainable AI error: {e}"
        )
        # -----------------------------
# DATA MINING / PATTERN DISCOVERY
# -----------------------------

elif page == "⛏️ Data Mining":

    st.title("⛏️ Data Mining & Pattern Discovery")

    st.write(
        "Explore important relationships, statistical patterns "
        "and patient characteristics from the healthcare dataset."
    )

    try:

        df = load_dataset()

        st.subheader(
            "Feature Correlation with Diabetes Outcome"
        )

        numeric_df = df.select_dtypes(
            include="number"
        )

        correlations = (
            numeric_df.corr()["Outcome"]
            .drop("Outcome")
            .sort_values(
                ascending=False
            )
        )

        correlation_df = (
            correlations
            .reset_index()
        )

        correlation_df.columns = [
            "Feature",
            "Correlation"
        ]

        correlation_df["Correlation"] = (
            correlation_df["Correlation"]
            .round(3)
        )

        st.dataframe(
            correlation_df,
            use_container_width=True
        )

        fig1 = px.bar(
            correlation_df,
            x="Feature",
            y="Correlation",
            title="Feature Correlation with Diabetes Outcome"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        st.divider()

        # Glucose pattern

        st.subheader(
            "Glucose Pattern Analysis"
        )

        glucose_pattern = (
            df.groupby("Outcome")["Glucose"]
            .agg([
                "mean",
                "median",
                "std"
            ])
            .round(2)
        )

        glucose_pattern.index = [
            "No Diabetes",
            "Diabetes"
        ]

        st.dataframe(
            glucose_pattern,
            use_container_width=True
        )

        st.divider()

        # BMI analysis

        st.subheader(
            "BMI Pattern Analysis"
        )

        bmi_mean = df["BMI"].mean()
        bmi_median = df["BMI"].median()
        bmi_std = df["BMI"].std()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Mean BMI",
                f"{bmi_mean:.2f}"
            )

        with col2:

            st.metric(
                "Median BMI",
                f"{bmi_median:.2f}"
            )

        with col3:

            st.metric(
                "BMI Std. Deviation",
                f"{bmi_std:.2f}"
            )

        st.divider()

        # Age groups

        st.subheader(
            "Age Group Analysis"
        )

        age_bins = [
            0,
            20,
            30,
            40,
            50,
            60,
            100
        ]

        age_labels = [
            "<20",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60+"
        ]

        age_group_df = df.copy()

        age_group_df["Age Group"] = pd.cut(
            age_group_df["Age"],
            bins=age_bins,
            labels=age_labels,
            right=False
        )

        age_outcome = (
            age_group_df
            .groupby(
                ["Age Group", "Outcome"],
                observed=False
            )
            .size()
            .reset_index(
                name="Patients"
            )
        )

        age_outcome["Outcome"] = (
            age_outcome["Outcome"]
            .map({
                0: "No Diabetes",
                1: "Diabetes"
            })
        )

        fig2 = px.bar(
            age_outcome,
            x="Age Group",
            y="Patients",
            color="Outcome",
            barmode="group",
            title="Diabetes Distribution by Age Group"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.divider()

        # Top correlations

        st.subheader(
            "Top 5 Important Correlations"
        )

        top_correlations = (
            correlations
            .abs()
            .sort_values(
                ascending=False
            )
            .head(5)
        )

        top_corr_df = pd.DataFrame(
            {
                "Feature": top_correlations.index,
                "Absolute Correlation":
                    top_correlations.values
            }
        )

        st.dataframe(
            top_corr_df,
            use_container_width=True
        )

        st.info(
            "Data mining helps identify patterns and relationships "
            "within patient health data that can support "
            "further healthcare analysis."
        )

    except Exception as e:

        st.error(
            f"Data mining error: {e}"
        )


# -----------------------------

                    
# PREDICTION HISTORY
# -----------------------------

elif page == "📜 History":

    st.title("📜 Prediction History")

    st.write(
        "View your previous diabetes risk predictions."
    )

    if not user_id:

        st.warning("User information not available.")

    else:

        try:

            response = requests.get(
                f"http://127.0.0.1:8000/prediction-history/{user_id}"
            )

            if response.status_code == 200:

                history = response.json()

                if not history:

                    st.info(
                        "No prediction history found."
                    )

                else:

                    history_df = pd.DataFrame(history)

                    # Show raw data first
                    st.subheader("Your Prediction Records")

                    # Find actual column names safely
                    prediction_column = None

                    for col in history_df.columns:

                        if col.lower() == "prediction":
                            prediction_column = col
                            break

                    probability_column = None

                    for col in history_df.columns:

                        if col.lower() in [
                            "risk_probability",
                            "risk probability"
                        ]:
                            probability_column = col
                            break

                    # Metrics

                    total_predictions = len(
                        history_df
                    )

                    if prediction_column:

                        higher_risk = (
                            history_df[
                                prediction_column
                            ]
                            .astype(str)
                            .str.contains(
                                "Higher",
                                case=False,
                                na=False
                            )
                            .sum()
                        )

                        lower_risk = (
                            history_df[
                                prediction_column
                            ]
                            .astype(str)
                            .str.contains(
                                "Lower",
                                case=False,
                                na=False
                            )
                            .sum()
                        )

                    else:

                        higher_risk = 0
                        lower_risk = 0

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Total Predictions",
                            total_predictions
                        )

                    with col2:

                        st.metric(
                            "Higher Risk",
                            int(higher_risk)
                        )

                    with col3:

                        st.metric(
                            "Lower Risk",
                            int(lower_risk)
                        )

                    st.divider()

                    # Rename columns only if they exist

                    rename_map = {
                        "glucose": "Glucose",
                        "blood_pressure": "Blood Pressure",
                        "bmi": "BMI",
                        "age": "Age",
                        "pregnancies": "Pregnancies",
                        "prediction": "Prediction",
                        "risk_probability": "Risk Probability",
                        "created_at": "Date"
                    }

                    history_df = history_df.rename(
                        columns=rename_map
                    )

                    # Convert probability

                    if "Risk Probability" in history_df.columns:

                        history_df[
                            "Risk Probability"
                        ] = pd.to_numeric(
                            history_df[
                                "Risk Probability"
                            ],
                            errors="coerce"
                        )

                        # Convert decimal to percentage
                        history_df[
                            "Risk Probability"
                        ] = (
                            history_df[
                                "Risk Probability"
                            ] * 100
                        ).round(2)

                    # Date formatting

                    if "Date" in history_df.columns:

                        history_df["Date"] = pd.to_datetime(
                            history_df["Date"],
                            errors="coerce"
                        )

                    # Display columns safely

                    display_columns = [
                        "Date",
                        "Pregnancies",
                        "Glucose",
                        "Blood Pressure",
                        "BMI",
                        "Age",
                        "Prediction",
                        "Risk Probability"
                    ]

                    display_columns = [
                        col
                        for col in display_columns
                        if col in history_df.columns
                    ]

                    st.dataframe(
                        history_df[
                            display_columns
                        ],
                        use_container_width=True
                    )

                    # Risk probability chart

                    if (
                        "Date" in history_df.columns
                        and
                        "Risk Probability"
                        in history_df.columns
                    ):

                        chart_df = history_df.dropna(
                            subset=[
                                "Date",
                                "Risk Probability"
                            ]
                        )

                        if not chart_df.empty:

                            st.subheader(
                                "Risk Probability Trend"
                            )

                            chart_df = chart_df.sort_values(
                                "Date"
                            )

                            fig = px.line(
                                chart_df,
                                x="Date",
                                y="Risk Probability",
                                markers=True,
                                title="Risk Probability Over Time"
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True
                            )

                    # Latest prediction

                    if (
                        "Prediction"
                        in history_df.columns
                        and not history_df.empty
                    ):

                        st.subheader(
                            "Latest Prediction"
                        )

                        if "Date" in history_df.columns:

                            latest = (
                                history_df
                                .sort_values(
                                    "Date",
                                    ascending=False
                                )
                                .iloc[0]
                            )

                        else:

                            latest = (
                                history_df.iloc[-1]
                            )

                        latest_prediction = str(
                            latest["Prediction"]
                        )

                        if "Higher" in latest_prediction:

                            st.error(
                                f"⚠️ {latest_prediction}"
                            )

                        else:

                            st.success(
                                f"✅ {latest_prediction}"
                            )

                        if (
                            "Risk Probability"
                            in history_df.columns
                        ):

                            probability = latest[
                                "Risk Probability"
                            ]

                            if pd.notna(probability):

                                st.metric(
                                    "Latest Risk Probability",
                                    f"{probability:.2f}%"
                                )

            else:

                st.error(
                    "Unable to load prediction history."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Backend is not running."
            )

        except Exception as e:

            st.error(
                f"History error: {e}"
            )

# -----------------------------
# END OF APPLICATION
# -----------------------------

st.sidebar.caption(
    "NIROGYA • AI-Powered Health Analytics"
)