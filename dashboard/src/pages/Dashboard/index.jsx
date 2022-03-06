import React, {useEffect, useState} from "react";
import './style.scss';
import {useParams, useNavigate} from 'react-router-dom';
import RealtimePlot from "../../components/RealtimePlot";
import Select from 'react-select';

export default function Dashboard() {
    const navigate = useNavigate();
    const {symbol} = useParams();
    const [symbols, setSymbols] = useState(null)
    const [symbolsError, setSymbolsError] = useState(false)

    useEffect(() => {
        fetch('/symbols').then(resp => resp.json()).then(resp => {
            setSymbols(resp.map(symbol => ({value: symbol, label: symbol})))
        }).catch(() => {
            setSymbolsError(true)
        })
    }, []);

    if (symbolsError) {
        return (
            <div className="dashboard">
                <div>Error while loading symbols. Reload page.</div>
            </div>
        )
    }

    if (symbols === null) {
        return (
            <div className="dashboard">
                <div>Loading symbols</div>
            </div>
        )
    }

    return (

        <div className="dashboard">
            <h1>Realtime plot</h1>
            <Select
                key={symbol}
                value={symbol || null}
                onChange={symbol => navigate(`/${symbol.value}`)}
                options={symbols}
            />
            {symbol ? <RealtimePlot symbol={symbol} height={350}/> : ''}
        </div>
    )
}

