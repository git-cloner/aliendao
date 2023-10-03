import React, { useCallback, useEffect, useImperativeHandle, useState } from 'react';
import AutoCompletion from "./AutoCompletion";

export default React.forwardRef((props, ref) => {
    const { onChange, onSend } = props;
    const [text, setText] = useState("");
    const [suggest, setSuggest] = useState([]);
    const [isSuggestShow, setSuggestShow] = useState(false);
    const [position, setPosition] = useState({ left: "20px", bottom: "60px" }); //left, bottom
    const autoCompletionRef = React.useRef(null);

    useImperativeHandle(ref, () => ({
        setText,
    }));

    const showSuggestItems = useCallback((suggests) => {
        if (suggests.length > 0) {
            setSuggest(suggests);
            setSuggestShow(true);
        } else {
            setSuggestShow(false);
        }
    }, []);


    async function getPrompts(val) {
        var xmlhttp = new XMLHttpRequest();
        var res = null
        xmlhttp.open("POST", 'https://gitclone.com/aiit/codegen_prompt/v1', false);
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=utf-8");
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                res = xmlhttp.responseText;
            }
        };
        xmlhttp.send(JSON.stringify({
            "context": val, "maxlength": 15, "samples": 5
        }));
        const res1 = JSON.parse(res);
        const result = JSON.parse(res1.result);
        for (let i = 0; i < result.length; i++) {
            result[i] = result[i].slice(0, result[i].indexOf('\n'));;
        }
        return result;
    }

    const handleChange = useCallback(async (ev) => {
        let val = ev.currentTarget.value;
        setText(val);
        onChange && onChange(val);

        let suggests = [];
        if (val.length > 0) {
            if (val.endsWith(".") || (val.endsWith("。"))) {
                suggests = await getPrompts(val.slice(0, -1));
            }
        }
        showSuggestItems(suggests);
    }, [showSuggestItems, onChange]);

    const send = useCallback((content) => {
        if (content) {
            onSend('text', content);
            setText('');
        }
        setSuggestShow(false);
    }, [onSend, setText]);

    const handleChoose = useCallback((suggest) => {
        if (suggest) {
            setText(suggest);
        }
        //不调用发送，用户可能需要修改选择的内容
        //send(suggest);
        setSuggestShow(false);
    }, [setText]);

    const handleSend = useCallback(() => {
        send(text)
    }, [send, text]);

    const handleKeydown = useCallback((e) => {
        let ret = false;
        if (isSuggestShow) {
            //只有在打开自动完成的时候交给自动完成接管事件
            ret = autoCompletionRef.current.onKeyEvent(e);
        }
        if (!ret) {
            if (!e.shiftKey && e.keyCode === 13) {
                send(text);
            }
        }
        if (!e.shiftKey && e.keyCode === 13) {
            e.preventDefault();
        }
    }, [isSuggestShow, send, text]);

    useEffect(() => {
        let node = document.getElementsByClassName("Composer")[0];
        setPosition({ left: "20px", "bottom": node.clientHeight + "px" })
    }, []);
    return <>
        <AutoCompletion
            ref={autoCompletionRef}
            show={isSuggestShow}
            items={suggest}
            position={position}
            onChoose={handleChoose} />
        <div className="Composer" ref={ref}>
            <div className="Composer-inputWrap">
                <div className="">
                    <textarea className="Input Input--outline Composer-input"
                        placeholder="shift + 回车换行，.或。提示" rows="1"
                        onKeyDown={handleKeydown}
                        enterKeyHint="send" value={text} onChange={handleChange}></textarea></div>
            </div>
            {text && <div className="Composer-actions">
                <button className="Btn Btn--primary Composer-sendBtn" type="button" onClick={handleSend}>发送</button>
            </div>}
        </div>
    </>
});