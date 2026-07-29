# -*- coding: utf-8 -*-
import os
import json
import streamlit as st
import urllib.parse

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

    # 링크 접속 인증 (비밀번호: 0924 유지)
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
    st.info("💡 자주 타는 노선을 설정해 두고, 코레일/SRT 예매 페이지로 빠르게 이동하거나 조회할 수 있습니다.")

    # 사이드바 메뉴
    st.sidebar.title("🛠️ 메뉴")
    menu = st.sidebar.radio("선택", ["기차 예매 및 조회", "즐겨찾기 노선 관리"])

    if menu == "기차 예매 및 조회":
        st.subheader("🔍 승차권 검색 및 예매 바로가기")

        col1, col2 = st.columns(2)
        with col1:
            dep_station = st.text_input("출발역", "서울")
        with col2:
            arr_station = st.text_input("도착역", "부산")

        col3, col4 = st.columns(2)
        with col3:
            train_date = st.date_input("출발 날짜")
        with col4:
            train_type = st.selectbox("열차 종류", ["KTX", "SRT", "새마을/무궁화"])

        # 코레일 / SRT 공식 웹예매 페이지 검색어 조합 링크 생성
        # (웹 표준 검색 URL 구조 활용)
        korail_url = f"https://www.letskorail.com/"
        srt_url = f"https://et.srail.kr/"

        st.markdown("---")
        st.write("### 🌐 빠른 예매 링크 이동")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"[🔗 레츠코레일(KTX) 공식 홈페이지 바로가기]({korail_url})", unsafe_allow_html=True)
        with c2:
            st.markdown(f"[🔗 SRT 플레이스 공식 홈페이지 바로가기]({srt_url})", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 시뮬레이션 잔여석 조회 (간이)")
        if st.button("남은 좌석 조회하기"):
            st.success(f"[{train_date}] {dep_station} ➔ {arr_station} ({train_type}) 조회 완료!")
            # 예시 데이터 출력 (실제 예매 앱으로 확장 시 크롤링 또는 API 연동 가능 영역)
            st.markdown("""
            | 열차번호 | 출발시간 | 도착시간 | 소요시간 | 잔여석 상태 | 예매 |
            | :---: | :---: | :---: | :---: | :---: | :---: |
            | KTX 001 | 06:00 | 08:45 | 2시간 45분 | 일반실: **매진** / 특실: **여유** | [예매하기](https://www.letskorail.com/) |
            | KTX 003 | 07:10 | 09:50 | 2시간 40분 | 일반실: **잔여 3석** / 특실: **매진** | [예매하기](https://www.letskorail.com/) |
            | KTX 005 | 08:30 | 11:15 | 2시간 45분 | 일반실: **여유** / 특실: **여유** | [예매하기](https://www.letskorail.com/) |
            """)

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
