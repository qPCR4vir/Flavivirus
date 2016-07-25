print 'Distance'
import Orange

samples=[ inst["Sample"] for inst in in_data ]

features= [Orange.feature.Continuous( str(virus) ) for virus in  samples ]
print features
#[Orange.feature.Continuo("Virus", values=values[:card])
#domain
#out_data=Orange.data.Table(i)
print len(features)


