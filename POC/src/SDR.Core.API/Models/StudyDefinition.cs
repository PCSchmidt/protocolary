using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace SDR.Core.API.Models
{
    public class StudyDefinition
    {
        [JsonPropertyName("id")]
        public string Id { get; set; }

        [JsonPropertyName("clinicalStudy")]
        public ClinicalStudy ClinicalStudy { get; set; }
    }

    public class ClinicalStudy
    {
        [JsonPropertyName("studyId")]
        public string StudyId { get; set; }

        [JsonPropertyName("studyTitle")]
        public string StudyTitle { get; set; }

        [JsonPropertyName("studyVersion")]
        public string StudyVersion { get; set; }

        [JsonPropertyName("studyPhase")]
        public CodedValue StudyPhase { get; set; }

        [JsonPropertyName("studyType")]
        public CodedValue StudyType { get; set; }

        [JsonPropertyName("studyDesigns")]
        public List<StudyDesign> StudyDesigns { get; set; }
    }

    public class StudyDesign
    {
        [JsonPropertyName("studyDesignId")]
        public string StudyDesignId { get; set; }

        [JsonPropertyName("studyDesignName")]
        public string StudyDesignName { get; set; }

        [JsonPropertyName("studyDesignDescription")]
        public string StudyDesignDescription { get; set; }

        [JsonPropertyName("interventionModel")]
        public CodedValue InterventionModel { get; set; }

        [JsonPropertyName("trialType")]
        public CodedValue TrialType { get; set; }

        [JsonPropertyName("trialIntentType")]
        public CodedValue TrialIntentType { get; set; }

        [JsonPropertyName("studyPopulations")]
        public List<StudyPopulation> StudyPopulations { get; set; }

        [JsonPropertyName("studyArms")]
        public List<StudyArm> StudyArms { get; set; }

        [JsonPropertyName("studyEpochs")]
        public List<StudyEpoch> StudyEpochs { get; set; }

        [JsonPropertyName("studyCells")]
        public List<StudyCell> StudyCells { get; set; }

        [JsonPropertyName("scheduleTimelines")]
        public List<ScheduleTimeline> ScheduleTimelines { get; set; }

        [JsonPropertyName("biomedicalConcepts")]
        public List<BiomedicalConcept> BiomedicalConcepts { get; set; }
    }

    public class CodedValue
    {
        [JsonPropertyName("code")]
        public string Code { get; set; }

        [JsonPropertyName("codeSystem")]
        public string CodeSystem { get; set; }

        [JsonPropertyName("codeSystemVersion")]
        public string CodeSystemVersion { get; set; }

        [JsonPropertyName("decode")]
        public string Decode { get; set; }
    }

    public class StudyPopulation
    {
        [JsonPropertyName("populationId")]
        public string PopulationId { get; set; }

        [JsonPropertyName("populationDescription")]
        public string PopulationDescription { get; set; }
    }

    public class StudyArm
    {
        [JsonPropertyName("studyArmId")]
        public string StudyArmId { get; set; }

        [JsonPropertyName("studyArmName")]
        public string StudyArmName { get; set; }

        [JsonPropertyName("studyArmType")]
        public CodedValue StudyArmType { get; set; }

        [JsonPropertyName("studyArmDescription")]
        public string StudyArmDescription { get; set; }
    }

    public class StudyEpoch
    {
        [JsonPropertyName("studyEpochId")]
        public string StudyEpochId { get; set; }

        [JsonPropertyName("studyEpochName")]
        public string StudyEpochName { get; set; }

        [JsonPropertyName("studyEpochDescription")]
        public string StudyEpochDescription { get; set; }

        [JsonPropertyName("studyEpochType")]
        public CodedValue StudyEpochType { get; set; }
    }

    public class StudyCell
    {
        [JsonPropertyName("studyCellId")]
        public string StudyCellId { get; set; }

        [JsonPropertyName("studyArmId")]
        public string StudyArmId { get; set; }

        [JsonPropertyName("studyEpochId")]
        public string StudyEpochId { get; set; }
    }

    public class ScheduleTimeline
    {
        [JsonPropertyName("scheduleTimelineId")]
        public string ScheduleTimelineId { get; set; }

        [JsonPropertyName("scheduleTimelineName")]
        public string ScheduleTimelineName { get; set; }

        [JsonPropertyName("scheduleTimelineDescription")]
        public string ScheduleTimelineDescription { get; set; }

        [JsonPropertyName("scheduleTimelineEntries")]
        public List<ScheduleTimelineEntry> ScheduleTimelineEntries { get; set; }
    }

    public class ScheduleTimelineEntry
    {
        [JsonPropertyName("timelineEntryId")]
        public string TimelineEntryId { get; set; }

        [JsonPropertyName("timelineEntryName")]
        public string TimelineEntryName { get; set; }

        [JsonPropertyName("timelineEntryDescription")]
        public string TimelineEntryDescription { get; set; }

        [JsonPropertyName("studyEpochId")]
        public string StudyEpochId { get; set; }

        [JsonPropertyName("timelineEntryDay")]
        public int TimelineEntryDay { get; set; }

        [JsonPropertyName("activities")]
        public List<Activity> Activities { get; set; }
    }

    public class Activity
    {
        [JsonPropertyName("activityId")]
        public string ActivityId { get; set; }

        [JsonPropertyName("activityName")]
        public string ActivityName { get; set; }

        [JsonPropertyName("activityDescription")]
        public string ActivityDescription { get; set; }

        [JsonPropertyName("biomedicalConceptIds")]
        public List<string> BiomedicalConceptIds { get; set; }

        [JsonPropertyName("definedProcedures")]
        public List<Procedure> DefinedProcedures { get; set; }
    }

    public class Procedure
    {
        [JsonPropertyName("procedureId")]
        public string ProcedureId { get; set; }

        [JsonPropertyName("procedureName")]
        public string ProcedureName { get; set; }

        [JsonPropertyName("procedureDescription")]
        public string ProcedureDescription { get; set; }
    }

    public class BiomedicalConcept
    {
        [JsonPropertyName("id")]
        public string Id { get; set; }

        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("label")]
        public string Label { get; set; }

        [JsonPropertyName("synonyms")]
        public List<string> Synonyms { get; set; }

        [JsonPropertyName("reference")]
        public string Reference { get; set; }

        [JsonPropertyName("code")]
        public CodedValue Code { get; set; }

        [JsonPropertyName("properties")]
        public List<BiomedicalConceptProperty> Properties { get; set; }
    }

    public class BiomedicalConceptProperty
    {
        [JsonPropertyName("id")]
        public string Id { get; set; }

        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("label")]
        public string Label { get; set; }

        [JsonPropertyName("isRequired")]
        public bool IsRequired { get; set; }

        [JsonPropertyName("isEnabled")]
        public bool IsEnabled { get; set; }

        [JsonPropertyName("datatype")]
        public string Datatype { get; set; }

        [JsonPropertyName("unitOfMeasure")]
        public string UnitOfMeasure { get; set; }

        [JsonPropertyName("minValue")]
        public double? MinValue { get; set; }

        [JsonPropertyName("maxValue")]
        public double? MaxValue { get; set; }

        [JsonPropertyName("code")]
        public CodedValue Code { get; set; }

        [JsonPropertyName("responseCodes")]
        public List<ResponseCode> ResponseCodes { get; set; }
    }

    public class ResponseCode
    {
        [JsonPropertyName("id")]
        public string Id { get; set; }

        [JsonPropertyName("isEnabled")]
        public bool IsEnabled { get; set; }

        [JsonPropertyName("code")]
        public CodedValue Code { get; set; }
    }
}
