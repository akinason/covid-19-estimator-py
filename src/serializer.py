from marshmallow import fields, Schema


class RegionSerializer(Schema):
    name = fields.Str(required=True)
    avgAge = fields.Float(required=True)
    avgDailyIncomeInUSD = fields.Float(required=True)
    avgDailyIncomePopulation = fields.Float(required=True)


class DataSerializer(Schema):
    region = fields.Nested(RegionSerializer(), required=True)
    periodType = fields.String(required=True)
    timeToElapse = fields.Integer(required=True)
    reportedCases = fields.Integer(required=True)
    population = fields.Integer(required=True)
    totalHospitalBeds = fields.Integer(required=True)
