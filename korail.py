# -*- coding: utf-8 -*-
import os
import json
import streamlit as st
import datetime

DATA_FILE = "train_data.json"

def save_data():
    try:
        data = {
            "favorites": st.session_state.get("favorites", [])
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"데이터 저장 중 오류 발생: {e}")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.favorites = data.get("favorites", [])
        except Exception as e:
            print(f"데이터 불러오기 중 오류 발생: {e}")

def main():
    st.set_page_config(
        page_title="간편 기차 예매 도우미",
        page_icon="🚄",
        layout="wide"
    )

    # 링크 접속 인증 (비밀번호: 0924)
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔒 접근 제한된 프로그램입니다")
        st.info("접속 비밀번호를 입력해주세요.")
        
        entered_password = st.text_input("접속 비밀번호 입력", type="password")
        if st.button("확인"):
            if entered_password == "0924":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("⚠️ 비밀번호가 올바르지 않습니다.")
        return

    if "favorites" not in st.session_state:
        st.session_state.favorites = []
        
    if "data_loaded" not in st.session_state:
        load_data()
        st.session_state.data_loaded = True

    st.title("🚄 내 손안의 간편 기차 예매 도우미")
    st.info("💡 브라우저 자동완성을 활용해 링크를 누르면 빠르게 로그인 및 예매를 진행할 수 있습니다.")

    st.sidebar.title("🛠️ 메뉴")
    menu = st.sidebar.radio("선택", ["기차 예매 및 조회", "즐겨찾기 노선 관리"])

    if menu == "기차 예매 및 조회":
        st.subheader("🔍 승차권 검색 및 맞춤 바로가기")

        col1, col2 = st.columns(2)
        with col1:
            dep_station = st.text_input("출발역", "서울")
        with col2:
            arr_station = st.text_input("도착역", "부산")

        col3, col4 = st.columns(2)
        with col3:
            train_date = st.date_input("출발 날짜", datetime.date.today())
        with col4:
            train_time = st.selectbox("출발 시간대", [
                "전체 시간", "00시~06시", "06시~10시", "10시~14시", 
                "14시~18시", "18시~22시", "22시~24시"
            ])

        st.markdown("---")
        st.subheader("🌐 원클릭 공식 예매 페이지 이동")
        st.write("버튼을 누르면 공식 예매 사이트로 이동합니다. (브라우저 자동완성 연동)")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            ### 🚄 KTX (코레일)
            * **출발역:** {dep_station}
            * **도착역:** {arr_station}
            * **날짜:** {train_date} ({train_time})
            """, unsafe_allow_html=True)
            st.markdown("[🔗 코레일 승차권 예매 바로가기](https://www.korail.com/ticket/main)", unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            ### 🚄 SRT (수서고속철도)
            * **출발역:** {dep_station}
            * **도착역:** {arr_station}
            * **날짜:** {train_date} ({train_time})
            """, unsafe_allow_html=True)
            st.markdown("[🔗 SRT 승차권 예매 바로가기](https://etk.srail.kr/main.do)", unsafe_allow_html=True)

        # 즐겨찾기 빠른 연동 섹션 추가
        if st.session_state.favorites:
            st.markdown("---")
            st.subheader("⭐ 내 즐겨찾기 노선으로 바로 예매하기")
            for fav in st.session_state.favorites:
                f_col1, f_col2, f_col3 = st.columns([2, 2, 1])
                with f_col1:
                    st.write(f"**{fav['name']}**")
                with f_col2:
                    st.write(f"{fav['dep']} ➔ {fav['arr']}")
                with f_col3:
                    st.markdown(f"[코레일 이동](https://www.korail.com/ticket/main)")

    elif menu == "즐겨찾기 노선 관리":
        st.subheader("⭐ 자주 가는 노선 즐겨찾기")

        with st.form("add_fav"):
            f_name = st.text_input("노선 별칭 (예: 주말 본가행)")
            f_dep = st.text_input("출발역", "서울")
            f_arr = st.text_input("도착역", "동대구")
            f_submitted = st.form_submit_button("즐겨찾기 추가")
            
            if f_submitted:
                if f_name.strip():
                    st.session_state.favorites.append({"name": f_name, "dep": f_dep, "arr": f_arr})
                    save_data()
                    st.success(f"'{f_name}' 노선이 저장되었습니다!")
                    st.rerun()

        st.divider()
        if st.session_state.favorites:
            st.write("### 📌 저장된 내 노선 목록")
            for idx, fav in enumerate(st.session_state.favorites):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.info(f"**{fav['name']}**: {fav['dep']} ➔ {fav['arr']}")
                with col_b:
                    if st.button("삭제", key=f"del_{idx}"):
                        st.session_state.favorites.pop(idx)
                        save_data()
                        st.rerun()
        else:
            st.info("등록된 즐겨찾기 노선이 없습니다.")

if __name__ == "__main__":
    main()
