import streamlit as st
import ast
import json
from streamlit_tree_select import tree_select

def robust_json_parser(json_str):
    try:
        # ast.literal_eval을 사용하여 파싱
        parsed_data = ast.literal_eval(json_str)
        return parsed_data, None
    except (SyntaxError, ValueError) as e:
        # 파싱 오류 발생 시 오류 메시지 반환
        return None, str(e)

def json_to_tree(json_obj, parent_key=''):
    if isinstance(json_obj, dict):
        return [
            {
                'label': f"{k}",
                'value': f"{parent_key}/{k}" if parent_key else k,
                'children': json_to_tree(v, f"{parent_key}/{k}" if parent_key else k)
            }
            for k, v in json_obj.items()
        ]
    elif isinstance(json_obj, list):
        return [
            {
                'label': f"[{i}]",
                'value': f"{parent_key}/{i}" if parent_key else str(i),
                'children': json_to_tree(v, f"{parent_key}/{i}" if parent_key else str(i))
            }
            for i, v in enumerate(json_obj)
        ]
    else:
        return []

st.set_page_config(layout="wide")

st.title("강화된 JSON 파서 & 트리 뷰어 (Pretty Print 포함)")

col1, col2 = st.columns(2)

with col1:
    st.header("JSON 입력")
    json_input = st.text_area("여기에 JSON을 입력하세요 (작은따옴표 허용):", height=300)

with col2:
    st.header("파싱된 JSON")
    if json_input:
        parsed_json, error = robust_json_parser(json_input)
        if error:
            st.error(f"JSON 파싱 오류: {error}")
            st.text("오류 위치:")
            lines = json_input.split('\n')
            for i, line in enumerate(lines):
                if str(i+1) in error:
                    st.markdown(f"**{i+1}: {line}**")
                else:
                    st.text(f"{i+1}: {line}")
        elif parsed_json:
            tabs = st.tabs(["트리 뷰", "Pretty Print"])
            
            with tabs[0]:
                tree_data = json_to_tree(parsed_json)
                selected = tree_select(tree_data)
                
                st.subheader("선택된 노드 정보:")
                st.json(selected)
            
            with tabs[1]:
                st.json(parsed_json)

    else:
        st.info("JSON을 입력하면 여기에 파싱 결과가 표시됩니다.")

st.sidebar.header("사용 방법")
st.sidebar.info(
    "1. 왼쪽 텍스트 영역에 JSON을 입력하세요. 작은따옴표(')로 작성된 JSON도 허용됩니다.\n"
    "2. 입력하면 자동으로 파싱되어 오른쪽에 표시됩니다.\n"
    "3. 파싱 오류가 발생하면 오류 메시지와 함께 오류 위치가 표시됩니다.\n"
    "4. 파싱된 JSON은 '트리 뷰'와 'Pretty Print' 탭으로 나누어 표시됩니다.\n"
    "5. 트리 뷰에서 노드를 선택하면 해당 노드의 정보가 아래에 표시됩니다."
)