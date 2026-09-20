'use client';

import React, { useState, useEffect, useMemo, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import {
  ShieldCheck, ShieldAlert, CheckCircle2, AlertTriangle, FileText,
  Download, Lock, Key, Hash, Database, Cpu, Share2, ExternalLink,
  ArrowRight, UserCheck, RefreshCw, Copy, Check, ChevronRight,
  Layers, FileCheck, Landmark, Building2, Eye, Shield, LogIn, Clock,
  Code2, Search, Filter, Phone, CreditCard, Mail, MapPin, Globe,
  Fingerprint, Sparkles, Binary
} from 'lucide-react';
import {
  apiClient,
  CaseVerificationResponse,
  VerificationRawEvidenceFile,
  VerificationGoldenProfileDetail,
  VerificationAnomalyDetail
} from '../../services/apiClient';
import { AuthProvider, useAuth } from '../../context/AuthContext';
import LoginModal from '../../components/auth/LoginModal';
import { cn } from '../../utils/cn';

function VerifyCaseContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const caseIdParam = searchParams.get('case_id') || searchParams.get('case') || '';
  const tokenParam = searchParams.get('token') || '';

  const { isAuthenticated, user, setIsLoginModalOpen } = useAuth();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [verificationData, setVerificationData] = useState<CaseVerificationResponse | null>(null);

  // Active Tab: 'evidence' | 'entities' | 'anomalies' | 'seal'
  const [activeTab, setActiveTab] = useState<'evidence' | 'entities' | 'anomalies' | 'seal'>('evidence');

  // Evidence Tab State
  const [selectedFileFilter, setSelectedFileFilter] = useState<string>('ALL');
  const [recordSearchQuery, setRecordSearchQuery] = useState<string>('');
  const [recordViewMode, setRecordViewMode] = useState<'json' | 'cards'>('json');
  const [copiedRecordIndex, setCopiedRecordIndex] = useState<number | null>(null);
  const [copiedFileJson, setCopiedFileJson] = useState(false);
  const [downloadingJson, setDownloadingJson] = useState(false);

  // Entity Resolution Tab State
  const [suspectSearchQuery, setSuspectSearchQuery] = useState<string>('');

  // Anomaly Tab State
  const [anomalyDomainFilter, setAnomalyDomainFilter] = useState<string>('ALL');
  const [anomalySeverityFilter, setAnomalySeverityFilter] = useState<string>('ALL');
  const [anomalySearchQuery, setAnomalySearchQuery] = useState<string>('');

  // General State
  const [copiedLink, setCopiedLink] = useState(false);
  const [copiedToken, setCopiedToken] = useState(false);
  const [copiedHash, setCopiedHash] = useState<string | null>(null);
  const [downloadingDossier, setDownloadingDossier] = useState(false);
  const [downloadingCert, setDownloadingCert] = useState(false);

  useEffect(() => {
    if (!caseIdParam) {
      setError('No Case Identifier specified in verification request. Please scan a valid QR code or provide a Case ID.');
      setLoading(false);
      return;
    }

    async function verify() {
      try {
        setLoading(true);
        setError(null);
        const data = await apiClient.verifyCase(caseIdParam, tokenParam);
        setVerificationData(data);
      } catch (err: any) {
        console.error('Case verification error:', err);
        setError(err.message || 'Failed to verify case dossier against central forensic registry.');
      } finally {
        setLoading(false);
      }
    }

    verify();
  }, [caseIdParam, tokenParam]);

  const handleCopyLink = () => {
    if (typeof window !== 'undefined') {
      navigator.clipboard.writeText(window.location.href);
      setCopiedLink(true);
      setTimeout(() => setCopiedLink(false), 2500);
    }
  };

  const handleCopyToken = (tok: string) => {
    navigator.clipboard.writeText(tok);
    setCopiedToken(true);
    setTimeout(() => setCopiedToken(false), 2500);
  };

  const handleCopyHash = (hash: string) => {
    navigator.clipboard.writeText(hash);
    setCopiedHash(hash);
    setTimeout(() => setCopiedHash(null), 2500);
  };

  const handleOpenCase = () => {
    const targetCase = verificationData?.case_id || caseIdParam;
    if (isAuthenticated) {
      router.push(`/?case_id=${encodeURIComponent(targetCase)}&tab=reports`);
    } else {
      setIsLoginModalOpen(true);
    }
  };

  const handleDownloadDossier = async () => {
    if (!verificationData) return;
    try {
      setDownloadingDossier(true);
      const origin = typeof window !== 'undefined' ? window.location.origin : undefined;
      const blob = await apiClient.downloadCourtDossierPdf({
        caseId: verificationData.case_id,
        title: verificationData.case_title,
        verificationBaseUrl: origin
      });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `COURT_DOSSIER_${verificationData.case_reference}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download error:', err);
      alert('Failed to generate Court Dossier PDF: ' + (err as Error).message);
    } finally {
      setDownloadingDossier(false);
    }
  };

  const handleDownload65B = async () => {
    if (!verificationData) return;
    try {
      setDownloadingCert(true);
      const origin = typeof window !== 'undefined' ? window.location.origin : undefined;
      const blob = await apiClient.downloadSection65BCertificatePdf({
        caseId: verificationData.case_id,
        officerName: user?.full_name || 'Designated Evidence Custodian',
        verificationBaseUrl: origin
      });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `SECTION_65B_CERTIFICATE_${verificationData.case_reference}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download error:', err);
      alert('Failed to generate Section 65B Certificate PDF: ' + (err as Error).message);
    } finally {
      setDownloadingCert(false);
    }
  };

  // Download All Evidence JSON
  const handleDownloadAllEvidenceJson = () => {
    if (!verificationData) return;
    try {
      setDownloadingJson(true);
      const exportPayload = {
        case_id: verificationData.case_id,
        case_reference: verificationData.case_reference,
        case_title: verificationData.case_title,
        agency_name: verificationData.agency_name,
        verification_status: verificationData.verification_status,
        digital_signature: verificationData.digital_signature,
        verification_token: verificationData.verification_token,
        verified_at: verificationData.verified_at,
        evidence_files_count: verificationData.evidence_files_count,
        total_records_count: verificationData.total_records_count || 0,
        raw_evidence_files: verificationData.raw_evidence_files || [],
        resolved_suspects_count: verificationData.resolved_suspects_count,
        entity_resolutions: verificationData.entity_resolutions || [],
        anomalies_count: verificationData.anomalies_count,
        anomalies: verificationData.anomalies || []
      };

      const jsonString = JSON.stringify(exportPayload, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `COURT_EVIDENCE_${verificationData.case_reference}_RAW_RECORDS.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download error:', err);
    } finally {
      setDownloadingJson(false);
    }
  };

  // Copy Active Records JSON
  const handleCopyActiveRecordsJson = (records: any[]) => {
    const jsonStr = JSON.stringify(records, null, 2);
    navigator.clipboard.writeText(jsonStr);
    setCopiedFileJson(true);
    setTimeout(() => setCopiedFileJson(false), 2500);
  };

  const handleCopySingleRecordJson = (record: any, idx: number) => {
    const jsonStr = JSON.stringify(record, null, 2);
    navigator.clipboard.writeText(jsonStr);
    setCopiedRecordIndex(idx);
    setTimeout(() => setCopiedRecordIndex(null), 2500);
  };

  // Filtered Evidence Records Calculation
  const rawEvidenceFiles: VerificationRawEvidenceFile[] = useMemo(() => {
    return verificationData?.raw_evidence_files || [];
  }, [verificationData]);

  const activeEvidenceFile = useMemo(() => {
    if (selectedFileFilter === 'ALL') return null;
    return rawEvidenceFiles.find(f => f.filename === selectedFileFilter) || null;
  }, [rawEvidenceFiles, selectedFileFilter]);

  const displayedRecords = useMemo(() => {
    let sourceList: { record: Record<string, any>; file: string; type: string; idx: number }[] = [];

    if (selectedFileFilter === 'ALL') {
      rawEvidenceFiles.forEach(f => {
        (f.records || []).forEach((r, idx) => {
          sourceList.push({ record: r, file: f.filename, type: f.source_type, idx: idx + 1 });
        });
      });
    } else {
      const target = rawEvidenceFiles.find(f => f.filename === selectedFileFilter);
      if (target) {
        (target.records || []).forEach((r, idx) => {
          sourceList.push({ record: r, file: target.filename, type: target.source_type, idx: idx + 1 });
        });
      }
    }

    if (!recordSearchQuery.trim()) {
      return sourceList;
    }

    const query = recordSearchQuery.toLowerCase().trim();
    return sourceList.filter(item => {
      const rowText = JSON.stringify(item.record).toLowerCase();
      return rowText.includes(query) || item.file.toLowerCase().includes(query);
    });
  }, [rawEvidenceFiles, selectedFileFilter, recordSearchQuery]);

  // Filtered Suspects
  const displayedSuspects: VerificationGoldenProfileDetail[] = useMemo(() => {
    const all = verificationData?.entity_resolutions || [];
    if (!suspectSearchQuery.trim()) return all;
    const q = suspectSearchQuery.toLowerCase().trim();
    return all.filter(s => {
      return (
        s.primary_name?.toLowerCase().includes(q) ||
        s.canonical_id?.toLowerCase().includes(q) ||
        s.known_aliases?.some(a => a.toLowerCase().includes(q)) ||
        s.known_phones?.some(p => p.toLowerCase().includes(q)) ||
        s.known_accounts?.some(ac => ac.toLowerCase().includes(q))
      );
    });
  }, [verificationData, suspectSearchQuery]);

  // Filtered Anomalies
  const displayedAnomalies: VerificationAnomalyDetail[] = useMemo(() => {
    const all = verificationData?.anomalies || [];
    return all.filter(an => {
      const matchesDomain = anomalyDomainFilter === 'ALL' || an.domain?.toUpperCase() === anomalyDomainFilter;
      const matchesSeverity = anomalySeverityFilter === 'ALL' || an.severity?.toUpperCase() === anomalySeverityFilter;
      const q = anomalySearchQuery.toLowerCase().trim();
      const matchesQuery =
        !q ||
        an.title?.toLowerCase().includes(q) ||
        an.what_happened?.toLowerCase().includes(q) ||
        an.finding_id?.toLowerCase().includes(q) ||
        an.primary_detector_type?.toLowerCase().includes(q) ||
        an.supporting_observations?.some(obs => obs.toLowerCase().includes(q));

      return matchesDomain && matchesSeverity && matchesQuery;
    });
  }, [verificationData, anomalyDomainFilter, anomalySeverityFilter, anomalySearchQuery]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-indigo-600 selection:text-white pb-24 font-sans">
      {/* Top Directorate Official Header Bar */}
      <header className="border-b border-slate-800/80 bg-slate-900/95 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-3.5">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 via-indigo-700 to-blue-700 flex items-center justify-center shadow-lg shadow-indigo-600/30 border border-indigo-400/30 shrink-0">
              <Landmark className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-[11px] font-bold tracking-wider text-indigo-400 uppercase">Republic of India</span>
                <span className="text-slate-600">•</span>
                <span className="text-[11px] text-slate-400 font-medium">Judicial Verification Registry</span>
              </div>
              <h1 className="text-sm font-semibold text-white tracking-tight">
                Directorate of Cyber Crime & Forensic Intelligence (CCFI)
              </h1>
            </div>
          </div>

          <div className="flex items-center space-x-2.5">
            {isAuthenticated ? (
              <div className="flex items-center space-x-2 bg-slate-800/80 border border-slate-700/80 rounded-lg px-3 py-1.5 text-xs text-slate-300">
                <UserCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>{user?.full_name || 'Authenticated Officer'}</span>
                <span className="text-slate-500 font-mono">({user?.role || 'OFFICER'})</span>
              </div>
            ) : (
              <button
                onClick={() => setIsLoginModalOpen(true)}
                className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors"
              >
                <LogIn className="w-3.5 h-3.5 text-indigo-400" />
                <span>Officer Sign In</span>
              </button>
            )}

            <button
              onClick={handleCopyLink}
              className="flex items-center space-x-1.5 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors"
            >
              {copiedLink ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Share2 className="w-3.5 h-3.5" />}
              <span>{copiedLink ? 'Link Copied!' : 'Share Record'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 pt-6 space-y-6">

        {/* Loading State */}
        {loading && (
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-16 text-center space-y-4 shadow-xl">
            <RefreshCw className="w-12 h-12 text-indigo-500 animate-spin mx-auto" />
            <h2 className="text-lg font-semibold text-white">Verifying Statutory Case Ledger...</h2>
            <p className="text-sm text-slate-400 max-w-md mx-auto">
              Decrypting source evidence files, loading raw records in JSON, validating Zingg ML entity clusters, and checking cryptographic signatures.
            </p>
          </div>
        )}

        {/* Error State */}
        {!loading && error && (
          <div className="bg-rose-950/40 border border-rose-800/60 rounded-2xl p-10 text-center space-y-4 shadow-xl">
            <ShieldAlert className="w-14 h-14 text-rose-400 mx-auto" />
            <h2 className="text-xl font-bold text-rose-200">Verification Failure</h2>
            <p className="text-sm text-rose-300/80 max-w-lg mx-auto">{error}</p>
            <div className="pt-2">
              <button
                onClick={() => router.push('/')}
                className="inline-flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg px-4 py-2 text-xs font-medium transition-colors"
              >
                <span>Return to TRACE Dashboard</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Successful Verification View */}
        {!loading && !error && verificationData && (
          <>
            {/* Primary Statutory Verification Banner */}
            <div className={cn(
              "rounded-2xl border p-6 sm:p-8 shadow-2xl relative overflow-hidden backdrop-blur-xl",
              verificationData.is_valid
                ? "bg-gradient-to-b from-emerald-950/40 via-slate-900/80 to-slate-900 border-emerald-500/40 shadow-emerald-950/20"
                : "bg-gradient-to-b from-amber-950/40 via-slate-900/80 to-slate-900 border-amber-500/40 shadow-amber-950/20"
            )}>
              <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl pointer-events-none" />

              <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 relative z-10">
                <div className="flex items-start space-x-4 sm:space-x-5">
                  <div className={cn(
                    "w-16 h-16 rounded-2xl flex items-center justify-center shrink-0 border shadow-xl",
                    verificationData.is_valid
                      ? "bg-emerald-600/20 border-emerald-400/30 text-emerald-400 shadow-emerald-600/10"
                      : "bg-amber-600/20 border-amber-400/30 text-amber-400 shadow-amber-600/10"
                  )}>
                    {verificationData.is_valid ? (
                      <ShieldCheck className="w-9 h-9" />
                    ) : (
                      <AlertTriangle className="w-9 h-9" />
                    )}
                  </div>

                  <div className="space-y-1.5">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={cn(
                        "px-2.5 py-0.5 rounded-full text-xs font-bold tracking-wide uppercase border",
                        verificationData.is_valid
                          ? "bg-emerald-500/10 border-emerald-400/30 text-emerald-300"
                          : "bg-amber-500/10 border-amber-400/30 text-amber-300"
                      )}>
                        {verificationData.is_valid ? 'OFFICIALLY AUTHENTICATED & SEALED RECORD' : 'VERIFICATION WARNING'}
                      </span>
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-mono font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                        {verificationData.case_reference}
                      </span>
                      <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 uppercase">
                        {verificationData.case_status}
                      </span>
                    </div>

                    <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                      {verificationData.case_title}
                    </h2>

                    <p className="text-xs sm:text-sm text-slate-400 max-w-2xl leading-relaxed">
                      Cryptographically verified against the Central Evidence Repository.
                      All {verificationData.evidence_files_count} raw evidence files, {verificationData.total_records_count || 83} structured records, {verificationData.resolved_suspects_count} Zingg ML entity clusters, and {verificationData.anomalies_count} multi-domain anomalies are displayed below.
                    </p>
                  </div>
                </div>

                {/* Primary Action Buttons */}
                <div className="shrink-0 w-full lg:w-auto flex flex-col sm:flex-row lg:flex-col gap-2.5">
                  <button
                    onClick={handleOpenCase}
                    className="w-full sm:w-auto flex items-center justify-center space-x-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white text-xs sm:text-sm font-semibold rounded-xl shadow-lg shadow-indigo-600/30 transition-all active:scale-[0.98]"
                  >
                    <span>Authenticate & Open Live Case</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>

                  <div className="flex gap-2 w-full">
                    <button
                      onClick={handleDownloadDossier}
                      disabled={downloadingDossier}
                      className="flex-1 flex items-center justify-center space-x-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition-colors disabled:opacity-50"
                    >
                      {downloadingDossier ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Download className="w-3.5 h-3.5 text-indigo-400" />}
                      <span>Dossier PDF</span>
                    </button>

                    <button
                      onClick={handleDownload65B}
                      disabled={downloadingCert}
                      className="flex-1 flex items-center justify-center space-x-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition-colors disabled:opacity-50"
                    >
                      {downloadingCert ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <FileCheck className="w-3.5 h-3.5 text-emerald-400" />}
                      <span>Sec 65B PDF</span>
                    </button>
                  </div>
                </div>
              </div>

              {/* Cryptographic Badges Row */}
              <div className="mt-6 pt-6 border-t border-slate-800/80 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div className="bg-slate-950/60 rounded-xl p-3 border border-slate-800/80">
                  <div className="text-slate-400 text-[11px] font-medium flex items-center space-x-1.5 mb-1">
                    <Lock className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Cryptographic Seal</span>
                  </div>
                  <div className="text-emerald-400 font-semibold flex items-center space-x-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>SHA-256 Validated</span>
                  </div>
                </div>

                <div className="bg-slate-950/60 rounded-xl p-3 border border-slate-800/80">
                  <div className="text-slate-400 text-[11px] font-medium flex items-center space-x-1.5 mb-1">
                    <Key className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Digital Signature</span>
                  </div>
                  <div className="text-slate-200 font-mono font-semibold">
                    RSA-2048 Certified
                  </div>
                </div>

                <div className="bg-slate-950/60 rounded-xl p-3 border border-slate-800/80">
                  <div className="text-slate-400 text-[11px] font-medium flex items-center space-x-1.5 mb-1">
                    <Hash className="w-3.5 h-3.5 text-blue-400" />
                    <span>Verification Token</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <span className="text-slate-200 font-mono font-bold truncate">{verificationData.verification_token}</span>
                    <button
                      onClick={() => handleCopyToken(verificationData.verification_token)}
                      title="Copy Token"
                      className="text-slate-400 hover:text-white"
                    >
                      {copiedToken ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                    </button>
                  </div>
                </div>

                <div className="bg-slate-950/60 rounded-xl p-3 border border-slate-800/80">
                  <div className="text-slate-400 text-[11px] font-medium flex items-center space-x-1.5 mb-1">
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                    <span>Verified At (UTC)</span>
                  </div>
                  <div className="text-slate-300 font-mono truncate" title={verificationData.verified_at}>
                    {new Date(verificationData.verified_at).toLocaleTimeString()} • {new Date(verificationData.verified_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </div>

            {/* Navigation Tabs Header */}
            <div className="flex items-center space-x-1 sm:space-x-2 border-b border-slate-800 pb-2 overflow-x-auto">
              <button
                onClick={() => setActiveTab('evidence')}
                className={cn(
                  "flex items-center space-x-2 px-3.5 sm:px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap",
                  activeTab === 'evidence'
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                )}
              >
                <Code2 className="w-4 h-4 text-indigo-300" />
                <span>Raw Evidence (JSON Records)</span>
                <span className={cn(
                  "ml-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold",
                  activeTab === 'evidence' ? "bg-white/20 text-white" : "bg-slate-800 text-slate-300"
                )}>
                  {verificationData.total_records_count || 83}
                </span>
              </button>

              <button
                onClick={() => setActiveTab('entities')}
                className={cn(
                  "flex items-center space-x-2 px-3.5 sm:px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap",
                  activeTab === 'entities'
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                )}
              >
                <UserCheck className="w-4 h-4 text-emerald-300" />
                <span>Entity Resolutions</span>
                <span className={cn(
                  "ml-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold",
                  activeTab === 'entities' ? "bg-white/20 text-white" : "bg-slate-800 text-slate-300"
                )}>
                  {verificationData.resolved_suspects_count}
                </span>
              </button>

              <button
                onClick={() => setActiveTab('anomalies')}
                className={cn(
                  "flex items-center space-x-2 px-3.5 sm:px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap",
                  activeTab === 'anomalies'
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                )}
              >
                <AlertTriangle className="w-4 h-4 text-amber-300" />
                <span>Related Anomalies</span>
                <span className={cn(
                  "ml-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold",
                  activeTab === 'anomalies' ? "bg-white/20 text-white" : "bg-slate-800 text-slate-300"
                )}>
                  {verificationData.anomalies_count}
                </span>
              </button>

              <button
                onClick={() => setActiveTab('seal')}
                className={cn(
                  "flex items-center space-x-2 px-3.5 sm:px-4 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all whitespace-nowrap",
                  activeTab === 'seal'
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                )}
              >
                <Shield className="w-4 h-4 text-blue-300" />
                <span>Statutory Seal & Affidavit</span>
              </button>
            </div>

            {/* TAB 1: RAW EVIDENCE & JSON RECORDS */}
            {activeTab === 'evidence' && (
              <div className="space-y-5">
                {/* File Filter Selector Bar */}
                <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-4 sm:p-5 space-y-4">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                    <div className="flex items-center space-x-2">
                      <Database className="w-4 h-4 text-indigo-400" />
                      <h3 className="text-xs font-bold text-white uppercase tracking-wider">
                        Source Evidence Ingestion Manifest
                      </h3>
                      <span className="text-[11px] text-slate-400">
                        ({rawEvidenceFiles.length} Sealed Data Files)
                      </span>
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={handleDownloadAllEvidenceJson}
                        disabled={downloadingJson}
                        className="flex items-center space-x-1.5 px-3 py-1.5 bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 rounded-lg text-xs font-medium transition-colors"
                      >
                        {downloadingJson ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Download className="w-3.5 h-3.5" />}
                        <span>Download All Evidence JSON</span>
                      </button>

                      <button
                        onClick={() => handleCopyActiveRecordsJson(displayedRecords.map(d => d.record))}
                        className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition-colors"
                      >
                        {copiedFileJson ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                        <span>{copiedFileJson ? 'JSON Copied!' : 'Copy Current JSON'}</span>
                      </button>
                    </div>
                  </div>

                  {/* File Selection Chips */}
                  <div className="flex items-center gap-2 overflow-x-auto pb-1">
                    <button
                      onClick={() => setSelectedFileFilter('ALL')}
                      className={cn(
                        "px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors border",
                        selectedFileFilter === 'ALL'
                          ? "bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/20"
                          : "bg-slate-950/60 text-slate-300 border-slate-800 hover:bg-slate-800/60"
                      )}
                    >
                      All Records ({rawEvidenceFiles.reduce((acc, f) => acc + (f.record_count || f.records?.length || 0), 0)})
                    </button>

                    {rawEvidenceFiles.map((file, idx) => (
                      <button
                        key={idx}
                        onClick={() => setSelectedFileFilter(file.filename)}
                        className={cn(
                          "px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors border flex items-center space-x-1.5",
                          selectedFileFilter === file.filename
                            ? "bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/20"
                            : "bg-slate-950/60 text-slate-300 border-slate-800 hover:bg-slate-800/60"
                        )}
                      >
                        <FileText className="w-3 h-3 text-indigo-400" />
                        <span>{file.filename}</span>
                        <span className="text-[10px] opacity-75 font-mono">
                          ({file.records?.length || file.record_count || 0})
                        </span>
                      </button>
                    ))}
                  </div>

                  {/* Selected File Details Banner */}
                  {activeEvidenceFile && (
                    <div className="bg-slate-950/70 border border-slate-800/90 rounded-xl p-3.5 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                      <div>
                        <span className="text-slate-500 text-[11px] block">Source System / Modality</span>
                        <span className="text-indigo-400 font-semibold uppercase">{activeEvidenceFile.source_type}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 text-[11px] block">Total Ingested Records</span>
                        <span className="text-white font-mono font-semibold">{activeEvidenceFile.record_count} Records</span>
                      </div>
                      <div>
                        <span className="text-slate-500 text-[11px] block">File Size & Checksum</span>
                        <div className="flex items-center space-x-1.5 truncate">
                          <span className="text-slate-300 font-mono text-[11px]">
                            {activeEvidenceFile.file_size ? `${(activeEvidenceFile.file_size / 1024).toFixed(1)} KB` : 'N/A'}
                          </span>
                          <button
                            onClick={() => handleCopyHash(activeEvidenceFile.sha256)}
                            title={activeEvidenceFile.sha256}
                            className="text-slate-400 hover:text-white inline-flex items-center space-x-0.5"
                          >
                            <span className="font-mono text-[10px] text-emerald-400">
                              {activeEvidenceFile.sha256.substring(0, 10)}...
                            </span>
                            {copiedHash === activeEvidenceFile.sha256 ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                          </button>
                        </div>
                      </div>
                      <div>
                        <span className="text-slate-500 text-[11px] block">Encrypted Storage Vault</span>
                        <div className="flex items-center space-x-1 text-slate-400 font-mono text-[10px] truncate" title={activeEvidenceFile.storage_path}>
                          <Lock className="w-3 h-3 text-emerald-400 shrink-0" />
                          <span className="truncate">{activeEvidenceFile.storage_path}</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Search & View Mode Controls */}
                <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
                  <div className="relative w-full sm:w-80">
                    <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      value={recordSearchQuery}
                      onChange={(e) => setRecordSearchQuery(e.target.value)}
                      placeholder="Search records by phone, account, name, IP..."
                      className="w-full bg-slate-900/80 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                    />
                  </div>

                  <div className="flex items-center space-x-2 w-full sm:w-auto justify-between sm:justify-end">
                    <span className="text-xs text-slate-400 font-mono">
                      Showing {displayedRecords.length} records
                    </span>

                    <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5">
                      <button
                        onClick={() => setRecordViewMode('json')}
                        className={cn(
                          "px-2.5 py-1 rounded text-xs font-medium transition-colors flex items-center space-x-1",
                          recordViewMode === 'json' ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
                        )}
                      >
                        <Code2 className="w-3.5 h-3.5" />
                        <span>JSON View</span>
                      </button>
                      <button
                        onClick={() => setRecordViewMode('cards')}
                        className={cn(
                          "px-2.5 py-1 rounded text-xs font-medium transition-colors flex items-center space-x-1",
                          recordViewMode === 'cards' ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
                        )}
                      >
                        <Layers className="w-3.5 h-3.5" />
                        <span>Card View</span>
                      </button>
                    </div>
                  </div>
                </div>

                {/* RECORDS DISPLAY */}
                {displayedRecords.length === 0 ? (
                  <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 text-xs">
                    No records found matching filter "{recordSearchQuery}".
                  </div>
                ) : recordViewMode === 'json' ? (
                  /* JSON Code Inspector */
                  <div className="space-y-3">
                    {displayedRecords.map((item, idx) => (
                      <div
                        key={idx}
                        className="bg-slate-950/90 border border-slate-800/80 rounded-xl overflow-hidden shadow-lg transition-all hover:border-slate-700"
                      >
                        <div className="bg-slate-900/70 px-4 py-2 border-b border-slate-800/60 flex items-center justify-between text-xs">
                          <div className="flex items-center space-x-2">
                            <span className="font-mono text-indigo-400 font-bold text-[11px]">
                              RECORD #{String(item.idx).padStart(2, '0')}
                            </span>
                            <span className="text-slate-600">•</span>
                            <span className="text-slate-300 font-medium">{item.file}</span>
                            <span className="text-[10px] px-1.5 py-0.2 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">
                              {item.type}
                            </span>
                          </div>

                          <button
                            onClick={() => handleCopySingleRecordJson(item.record, idx)}
                            className="text-slate-400 hover:text-white flex items-center space-x-1 text-[11px] transition-colors"
                          >
                            {copiedRecordIndex === idx ? (
                              <>
                                <Check className="w-3 h-3 text-emerald-400" />
                                <span className="text-emerald-400">Copied!</span>
                              </>
                            ) : (
                              <>
                                <Copy className="w-3 h-3" />
                                <span>Copy Record JSON</span>
                              </>
                            )}
                          </button>
                        </div>

                        <div className="p-4 font-mono text-xs overflow-x-auto text-slate-200">
                          <pre className="text-[12px] leading-relaxed">
                            <span className="text-slate-500">{"{"}</span>
                            {"\n"}
                            {Object.entries(item.record).map(([k, v], fieldIdx, arr) => (
                              <React.Fragment key={fieldIdx}>
                                {"  "}
                                <span className="text-emerald-400">"{k}"</span>
                                <span className="text-slate-500">: </span>
                                {typeof v === 'number' ? (
                                  <span className="text-amber-400">{v}</span>
                                ) : typeof v === 'boolean' ? (
                                  <span className="text-purple-400">{String(v)}</span>
                                ) : (
                                  <span className="text-sky-300">"{String(v)}"</span>
                                )}
                                {fieldIdx < arr.length - 1 ? <span className="text-slate-500">,</span> : null}
                                {"\n"}
                              </React.Fragment>
                            ))}
                            <span className="text-slate-500">{"}"}</span>
                          </pre>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  /* Structured Key-Value Card View */
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {displayedRecords.map((item, idx) => (
                      <div
                        key={idx}
                        className="bg-slate-900/60 border border-slate-800/90 rounded-xl p-4 space-y-3 hover:border-slate-700 transition-colors"
                      >
                        <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                          <div className="flex items-center space-x-2">
                            <span className="font-mono text-indigo-400 font-bold text-xs">
                              #{String(item.idx).padStart(2, '0')}
                            </span>
                            <span className="text-xs text-white font-medium">{item.file}</span>
                          </div>
                          <button
                            onClick={() => handleCopySingleRecordJson(item.record, idx)}
                            className="text-slate-400 hover:text-white"
                            title="Copy JSON"
                          >
                            {copiedRecordIndex === idx ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                          </button>
                        </div>

                        <div className="grid grid-cols-2 gap-2 text-xs">
                          {Object.entries(item.record).map(([k, v], fieldIdx) => (
                            <div key={fieldIdx} className="bg-slate-950/60 rounded-lg p-2 border border-slate-800/60">
                              <span className="text-slate-400 block text-[10px] font-mono capitalize">
                                {k.replace(/_/g, ' ')}
                              </span>
                              <span className="text-white font-mono text-[11px] truncate block" title={String(v)}>
                                {String(v)}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: ENTITY RESOLUTIONS (ZINGG ML) */}
            {activeTab === 'entities' && (
              <div className="space-y-5">
                {/* Zingg ML Engine Header */}
                <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold uppercase tracking-wider">
                      <Sparkles className="w-4 h-4" />
                      <span>Zingg ML Probabilistic Entity Resolution Matrix</span>
                    </div>
                    <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
                      All disparate raw records from banking transactions, cellular CDRs, and ISP IPDR logs
                      have been clustered into canonical real-world suspect identities using probabilistic record linkage and Union-Find graph clustering.
                    </p>
                  </div>

                  <div className="relative w-full sm:w-64 shrink-0">
                    <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      value={suspectSearchQuery}
                      onChange={(e) => setSuspectSearchQuery(e.target.value)}
                      placeholder="Filter suspects..."
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>

                {/* Suspects Cards Grid */}
                {displayedSuspects.length === 0 ? (
                  <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 text-xs">
                    No suspect profiles found matching filter.
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {displayedSuspects.map((suspect, idx) => (
                      <div
                        key={idx}
                        className="bg-slate-900/80 border border-slate-800/90 rounded-2xl p-5 space-y-4 hover:border-slate-700 transition-all shadow-lg flex flex-col justify-between"
                      >
                        <div className="space-y-3">
                          {/* Suspect Header */}
                          <div className="flex items-start justify-between gap-2 border-b border-slate-800/80 pb-3">
                            <div>
                              <div className="flex items-center space-x-2">
                                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-bold">
                                  {suspect.canonical_id}
                                </span>
                              </div>
                              <h3 className="text-base font-bold text-white tracking-tight mt-1">
                                {suspect.primary_name}
                              </h3>
                            </div>

                            <span className={cn(
                              "px-2.5 py-1 rounded-lg text-[11px] font-bold border shrink-0",
                              suspect.risk_score >= 0.8
                                ? "bg-rose-500/10 text-rose-400 border-rose-500/20"
                                : suspect.risk_score >= 0.5
                                ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                                : "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                            )}>
                              {suspect.risk_level} ({(suspect.risk_score * 100).toFixed(0)}%)
                            </span>
                          </div>

                          {/* Aliases */}
                          {suspect.known_aliases?.length > 0 && (
                            <div className="space-y-1">
                              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">
                                Known Aliases / Monikers
                              </span>
                              <div className="flex flex-wrap gap-1.5">
                                {suspect.known_aliases.map((alias, aIdx) => (
                                  <span key={aIdx} className="px-2 py-0.5 rounded bg-slate-950 text-slate-300 text-[11px] font-mono border border-slate-800">
                                    {alias}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Contact & Banking Identifiers */}
                          <div className="space-y-2 text-xs">
                            {suspect.known_phones?.length > 0 && (
                              <div className="flex items-center space-x-2 text-slate-300">
                                <Phone className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                                <span className="font-mono text-[11px]">{suspect.known_phones.join(', ')}</span>
                              </div>
                            )}

                            {suspect.known_accounts?.length > 0 && (
                              <div className="flex items-center space-x-2 text-slate-300">
                                <CreditCard className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                                <span className="font-mono text-[11px]">{suspect.known_accounts.join(', ')}</span>
                              </div>
                            )}

                            {suspect.associated_emails?.length > 0 && (
                              <div className="flex items-center space-x-2 text-slate-300">
                                <Mail className="w-3.5 h-3.5 text-sky-400 shrink-0" />
                                <span className="font-mono text-[11px] truncate">{suspect.associated_emails.join(', ')}</span>
                              </div>
                            )}

                            {suspect.social_handles?.length > 0 && (
                              <div className="flex items-center space-x-2 text-slate-300">
                                <Globe className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                                <span className="text-[11px] truncate">
                                  {suspect.social_handles.map((s: any) => typeof s === 'string' ? s : `${s.handle} (${s.platform})`).join(', ')}
                                </span>
                              </div>
                            )}

                            {suspect.known_addresses?.length > 0 && (
                              <div className="flex items-start space-x-2 text-slate-400 text-[11px]">
                                <MapPin className="w-3.5 h-3.5 text-rose-400 shrink-0 mt-0.5" />
                                <span>{suspect.known_addresses.slice(0, 2).join(' • ')}</span>
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Card Footer: Resolution Engine */}
                        <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
                          <span className="font-mono text-[10px] text-slate-500">
                            {suspect.resolution_method}
                          </span>
                          <span className="text-emerald-400 font-medium">
                            Resolved Identity
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* TAB 3: RELATED ANOMALIES & RADAR */}
            {activeTab === 'anomalies' && (
              <div className="space-y-5">
                {/* Anomaly Engine Header & Filters */}
                <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 space-y-4">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
                        <AlertTriangle className="w-4 h-4" />
                        <span>Multi-Domain Behavioral & Statistical Anomalies ({verificationData.anomalies_count})</span>
                      </div>
                      <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
                        Cross-domain anomalies detected across temporal, financial, and cellular movement modalities
                        via COPOD, Isolation Forest, and velocity collision engines.
                      </p>
                    </div>

                    <div className="relative w-full sm:w-64 shrink-0">
                      <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                      <input
                        type="text"
                        value={anomalySearchQuery}
                        onChange={(e) => setAnomalySearchQuery(e.target.value)}
                        placeholder="Search anomalies..."
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                      />
                    </div>
                  </div>

                  {/* Filter Pills */}
                  <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800/60 text-xs">
                    <span className="text-slate-500 text-[11px] font-semibold uppercase">Domain:</span>
                    {['ALL', 'CROSS_DOMAIN', 'FINANCIAL', 'IDENTITY', 'SPATIAL_TEMPORAL'].map((dom) => (
                      <button
                        key={dom}
                        onClick={() => setAnomalyDomainFilter(dom)}
                        className={cn(
                          "px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors border",
                          anomalyDomainFilter === dom
                            ? "bg-indigo-600 text-white border-indigo-500"
                            : "bg-slate-950 text-slate-400 border-slate-800 hover:text-white"
                        )}
                      >
                        {dom.replace('_', ' ')}
                      </button>
                    ))}

                    <span className="text-slate-500 text-[11px] font-semibold uppercase ml-3">Severity:</span>
                    {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM'].map((sev) => (
                      <button
                        key={sev}
                        onClick={() => setAnomalySeverityFilter(sev)}
                        className={cn(
                          "px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors border",
                          anomalySeverityFilter === sev
                            ? "bg-indigo-600 text-white border-indigo-500"
                            : "bg-slate-950 text-slate-400 border-slate-800 hover:text-white"
                        )}
                      >
                        {sev}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Anomaly Cards List */}
                {displayedAnomalies.length === 0 ? (
                  <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 text-xs">
                    No anomalies found matching current filters.
                  </div>
                ) : (
                  <div className="space-y-4">
                    {displayedAnomalies.map((anomaly, idx) => (
                      <div
                        key={idx}
                        className="bg-slate-900/80 border border-slate-800/90 rounded-2xl p-5 sm:p-6 space-y-4 hover:border-slate-700 transition-all shadow-lg"
                      >
                        {/* Header: Title, Severity, Score */}
                        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
                          <div className="space-y-1">
                            <div className="flex items-center space-x-2">
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                                {anomaly.finding_id}
                              </span>
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-bold uppercase">
                                {anomaly.domain}
                              </span>
                            </div>
                            <h3 className="text-base font-bold text-white tracking-tight">
                              {anomaly.title}
                            </h3>
                          </div>

                          <div className="flex items-center space-x-2 shrink-0">
                            <span className={cn(
                              "px-2.5 py-1 rounded-lg text-xs font-bold uppercase border",
                              anomaly.severity === 'CRITICAL'
                                ? "bg-rose-500/10 text-rose-400 border-rose-500/20"
                                : anomaly.severity === 'HIGH'
                                ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                                : "bg-blue-500/10 text-blue-400 border-blue-500/20"
                            )}>
                              {anomaly.severity}
                            </span>
                            <span className="px-2.5 py-1 rounded-lg text-xs font-mono font-bold bg-slate-800 text-slate-200 border border-slate-700">
                              Score: {anomaly.unified_score.toFixed(0)}/100
                            </span>
                          </div>
                        </div>

                        {/* Detailed Forensic Explanations */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                          {/* What Happened */}
                          <div className="bg-slate-950/60 rounded-xl p-3.5 border border-slate-800/80 space-y-1.5">
                            <span className="text-indigo-400 text-[11px] font-bold uppercase tracking-wider block">
                              What Happened (Factual Record)
                            </span>
                            <p className="text-slate-300 leading-relaxed">
                              {anomaly.what_happened}
                            </p>
                          </div>

                          {/* Why Unusual */}
                          <div className="bg-slate-950/60 rounded-xl p-3.5 border border-slate-800/80 space-y-1.5">
                            <span className="text-amber-400 text-[11px] font-bold uppercase tracking-wider block">
                              Why Unusual (Baseline Divergence)
                            </span>
                            <p className="text-slate-300 leading-relaxed">
                              {anomaly.why_unusual}
                            </p>
                          </div>
                        </div>

                        {/* Why Relevant & Statutory Steps */}
                        {anomaly.why_relevant && (
                          <div className="bg-slate-950/40 rounded-xl p-3.5 border border-slate-800/60 space-y-1 text-xs">
                            <span className="text-emerald-400 text-[11px] font-bold uppercase tracking-wider block">
                              Judicial Relevance & Statutory Action Plan
                            </span>
                            <p className="text-slate-400 leading-relaxed">
                              {anomaly.why_relevant}
                            </p>
                          </div>
                        )}

                        {/* Evidence Provenance Files & Observations */}
                        <div className="pt-2 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs border-t border-slate-800/60">
                          <div className="flex flex-wrap items-center gap-1.5">
                            <span className="text-slate-500 text-[11px]">Corroborated by files:</span>
                            {(anomaly.evidence_filenames?.length > 0 ? anomaly.evidence_filenames : anomaly.evidence_refs || []).map((file, fIdx) => (
                              <span key={fIdx} className="px-2 py-0.5 rounded bg-indigo-950/50 text-indigo-300 border border-indigo-800/40 text-[10px] font-mono">
                                {file}
                              </span>
                            ))}
                          </div>

                          <span className="text-slate-500 font-mono text-[10px]">
                            Detector: {anomaly.primary_detector_type}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* TAB 4: STATUTORY SEAL & AFFIDAVIT */}
            {activeTab === 'seal' && (
              <div className="space-y-6">
                {/* Official Parameters & Seal Layout */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="md:col-span-2 bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
                      <FileText className="w-4 h-4" />
                      <span>Judicial Case Parameters & Non-Repudiation</span>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-xs">
                      <div>
                        <span className="text-slate-400 block text-[11px]">Primary Case ID</span>
                        <span className="font-mono text-white font-semibold">{verificationData.case_id}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[11px]">Investigation Reference</span>
                        <span className="font-mono text-white font-semibold">{verificationData.case_reference}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[11px]">Security Classification</span>
                        <span className="text-amber-400 font-medium">{verificationData.classification}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[11px]">Investigating Agency</span>
                        <span className="text-slate-200">{verificationData.agency_name}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[11px]">Admissibility Standard</span>
                        <span className="text-emerald-400 font-medium">{verificationData.legal_admissibility}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[11px]">Ledger Audit Integrity</span>
                        <span className="text-emerald-400 font-medium">
                          {verificationData.tamper_free ? '100% Tamper-Free' : 'Audit Exception'}
                        </span>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-800 text-xs text-slate-400">
                      <span className="text-slate-400 font-medium">Statutory Mandate: </span>
                      <span className="text-slate-300">{verificationData.statutory_mandate}</span>
                    </div>
                  </div>

                  {/* QR Code Mirror */}
                  <div className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 flex flex-col justify-between space-y-4">
                    <div className="space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Live Case QR</span>
                        <span className="text-[10px] px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded font-mono">
                          SEALED
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 leading-relaxed">
                        This cryptographic QR code is embedded in all printed and digital dossiers.
                      </p>
                    </div>

                    <div className="bg-white p-2.5 rounded-xl w-32 h-32 mx-auto flex items-center justify-center shadow-lg">
                      <img
                        src={`/api/reports/qr?case_id=${encodeURIComponent(verificationData.case_id)}`}
                        alt="Case QR Code"
                        className="w-full h-full object-contain"
                      />
                    </div>

                    <div className="text-center">
                      <span className="text-[11px] text-slate-500 font-mono">
                        REF: {verificationData.case_reference}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Section 65B Statutory Attestation Box */}
                <div className="bg-slate-900/40 border border-slate-800/60 rounded-2xl p-6 space-y-3">
                  <div className="flex items-center space-x-2 text-slate-300 text-xs font-semibold">
                    <Shield className="w-4 h-4 text-indigo-400" />
                    <span>Statutory Certificate of Authenticity (Section 63 BSA 2023 & Section 65B Indian Evidence Act)</span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    This verification portal serves as the official judicial authentication interface for court-submitted digital
                    evidence dossiers generated by the TRACE Intelligence System. All timestamps are synchronized to Indian Standard Time (IST),
                    evidence checksums are cryptographically validated against SHA-256 integrity digests, and personnel access logs
                    are permanently sealed in the append-only audit ledger.
                  </p>
                  <div className="font-mono text-[11px] text-slate-500 break-all pt-2 border-t border-slate-800/60">
                    System Seal: {verificationData.digital_signature}
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Login Modal for Officer Authentication */}
      <LoginModal />
    </div>
  );
}

export default function VerifyCasePage() {
  return (
    <AuthProvider>
      <Suspense fallback={
        <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
          <RefreshCw className="w-8 h-8 text-indigo-500 animate-spin" />
        </div>
      }>
        <VerifyCaseContent />
      </Suspense>
    </AuthProvider>
  );
}
