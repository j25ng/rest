import streamlit as st
import pandas as pd
import requests
import time


@st.dialog("Update Data")
def update(p, id):
    update_first = st.text_input("First Name", p["firstName"])
    update_last = st.text_input("Last Name", p["lastName"])

    if st.button("Update", key="update_button"):
        data = {
            "firstName": update_first,
            "lastName": update_last,
        }

        response = requests.put(
            f"http://localhost:8080/people/{id}",
            json=data,
        )

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            st.success("데이터가 성공적으로 업데이트되었습니다.")
        else:
            st.error("데이터 업데이트에 실패했습니다.")


@st.dialog("Insert Data")
def insert():
    insert_first = st.text_input("First Name", placeholder="First Name")
    insert_last = st.text_input("Last Name", placeholder="Last Name")

    if st.button("Submit", key="submit_button"):
        data = {"firstName": insert_first, "lastName": insert_last}

        response = requests.post("http://localhost:8080/people", json=data)
        if response.status_code == 201:
            st.success("데이터가 삽입되었습니다.")
        else:
            st.error("데이터 삽입에 실패했습니다.")
        time.sleep(1)
        st.rerun()


st.title("PERSON")

data = requests.get(f"http://localhost:8080/people").json()
df = pd.DataFrame(data)["_embedded"]["people"]


if len(df) > 0:
    df = pd.DataFrame(df)

    # id 값만 추출, 컬럼추가
    df["id"] = df["_links"].apply(lambda x: x["self"]["href"].split("/")[-1])
    df = df[["id", "firstName", "lastName"]]

    id = st.selectbox("ID를 선택하세요", df["id"])

    if st.button("Select", key="select_button", use_container_width=True):
        p = df[df["id"] == id].iloc[0]
        update(p, id)

    if st.button("Delete", key="delete_button", use_container_width=True):
        response = requests.delete(f"http://localhost:8080/people/{id}")

        if response.status_code == 200:
            st.success("데이터가 삭제되었습니다.")
        else:
            st.error("데이터 삭제에 실패했습니다.")
        time.sleep(1)
        st.rerun()

else:
    st.warning("데이터가 없습니다.")

if st.button("Insert", key="insert_button", use_container_width=True):
    insert()
