package decoders

import (
	"fmt"
	"time"
)

func DecodeTimeRange(startTime string, endTime string) (*time.Time, *time.Time, error) {
	parseTime := func(s string) (time.Time, error) {
		t, err := time.Parse(time.RFC3339, s)
		if err == nil {
			return t, nil
		}
		layoutNaive := "2006-01-02T15:04:05"
		if len(s) > 19 {
			layoutNaive = "2006-01-02T15:04:05.999999"
		}

		return time.Parse(layoutNaive, s)
	}

	parsedStartTime, err := parseTime(startTime)
	if err != nil {
		return nil, nil, fmt.Errorf("error parsing startTime ('%s'): %v", startTime, err)
	}

	parsedEndTime, err := parseTime(endTime)
	if err != nil {
		return nil, nil, fmt.Errorf("error parsing endTime ('%s'): %v", endTime, err)
	}

	return &parsedStartTime, &parsedEndTime, nil
}
