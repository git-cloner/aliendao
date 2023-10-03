import React, {useCallback, useImperativeHandle, useState} from "react";

export default React.forwardRef((props, ref) => {
    const {show, items, onChoose, position, showClose=true} = props;
    const [selectedIndex, setSelectedIndex] = useState(0);

    const chooseNode = useCallback((node)=>{
        let content = node.dataset['content'];
        onChoose && onChoose(content || '');
    }, [onChoose]);

    const chooseItem = useCallback((ev)=>{
        let node = ev.currentTarget;
        chooseNode(node);
    }, [chooseNode]);

    const onKeyEvent = useCallback((e)=>{

        let index = 0;
        let max =  items.length;
        let type = e.key;

        if(type==="ArrowUp"){
            index = Math.max(selectedIndex-1, 0);
            setSelectedIndex(index);
            return true;
        }else if(type==="ArrowDown") {
            index = Math.min(selectedIndex + 1, max);
            setSelectedIndex(index);
            return true;
        }else if(!e.shiftKey && type==="Enter") {
            let lis = document.getElementsByClassName("completion-item active");
            if (lis.length > 0) {
                chooseNode(lis[0]);
            }
            return true;
        }
        return false;
    }, [selectedIndex,chooseNode, items]);

    const handleClose = useCallback(()=>{
        onChoose && onChoose('');
    },[onChoose]);

    useImperativeHandle(ref, ()=>({
        onKeyEvent
    }));

    return <>
        {
            show && <div className={"auto-completion"} ref={ref} style={{left: position.left, bottom: position.bottom}}>
                {showClose && <i className={"close"} onClick={handleClose}>x</i>}
                <ul>
                    {
                        items.map((n, i) => {
                            return <li key={i} className={`completion-item ${selectedIndex===i?"active":""}`} data-content={n} onClick={chooseItem}>{n}</li>
                        })
                    }
                </ul>
            </div>
        }
    </>

});