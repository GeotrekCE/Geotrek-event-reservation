const nbAnimations = {
  chart: {
    type: 'column',
  },
  title: {
    text: 'Nombre d\'animations par mois',
  },
  xAxis: {
    title: {
      text: null,
    },
  },
  yAxis: {
    min: 0,
    title: {
      text: 'Nb animations',
      align: 'high',
    },
    labels: {
      overflow: 'justify',
    },
  },
  credits: {
    enabled: false,
  },
  api_url: 'stats/charts/nb_day_before_resa',
  series: []
}

const nbDayBeforeResa = {
  chart: {
    type: 'spline',
  },
  title: {
    text: 'Nombre de jours avant reservation',
  },
  xAxis: {
    title: {
      text: null,
    },
  },
  yAxis: {
    min: 0,
    title: {
      text: 'Nb jours',
      align: 'high',
    },
    labels: {
      overflow: 'justify',
    },
  },
  credits: {
    enabled: false,
  },
  series: [
    {
      name: '2022',
      data: [
        [0, 20], [1, 54], [2, 31], [3, 21], [4, 18], [5, 12], [6, 17], [7, 20], [8, 9], [9, 12],
        [10, 13], [11, 6], [12, 2], [13, 8], [14, 11], [15, 5], [16, 8], [17, 5], [18, 4], [19, 4],
        [20, 5], [21, 3], [22, 3], [23, 1], [24, 2], [27, 2], [28, 3], [29, 3], [30, 5], [31, 2],
        [32, 1], [33, 1], [34, 1], [35, 9], [36, 3], [38, 1], [43, 1], [44, 1], [46, 3], [47, 2],
        [48, 1]
      ]
    }
  ]
}
export { nbAnimations, nbDayBeforeResa, }
