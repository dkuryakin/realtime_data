import React, {useEffect, useRef} from "react";
import './style.scss';
import useWebSocket from 'react-use-websocket';
import ReactApexChart from 'react-apexcharts'
import ApexCharts from 'apexcharts'

export default function RealtimePlot({symbol, height}) {
    const id = `realtime-${symbol}`
    const options = {
        chart: {
            id,
            height,
            type: 'line',
            animations: {
                enabled: true,
                easing: 'linear',
                dynamicAnimation: {
                    speed: 1000
                }
            },
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            }
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        title: {
            text: `Realtime plot: ${symbol}`,
            align: 'left'
        },
        markers: {
            size: 0
        },
        xaxis: {
            type: 'datetime',
            range: 1000 * 300,
        },
        yaxis: {
            //max: 1
        },
        legend: {
            show: false
        },
    }

    const didUnmount = useRef(false);
    const data = useRef([]);

    useWebSocket(`ws://${window.location.host}/price_events/${symbol}`, {
        onOpen: (e) => {
            console.log('ws connected')
            data.current = []
        },
        onMessage: (e) => {
            const messages = JSON.parse(e.data)
            messages.forEach(({price, timestamp}) => {
                data.current.push([parseInt(timestamp * 1000), price])
            })
            ApexCharts.exec(id, 'updateSeries', [{data: data.current}])
        },
        shouldReconnect: (closeEvent) => {
            return didUnmount.current === false;
        },
        reconnectAttempts: 86400,
        reconnectInterval: 1000,
    });


    useEffect(() => {
        return () => {
            didUnmount.current = true;
            console.log('ws disconnected')
        };
    }, []);


    return (
        <div className="chart">
            <ReactApexChart
                key={id}
                options={options}
                series={[{data: []}]}
                type="line"
                height={height}
            />
        </div>
    )
}

